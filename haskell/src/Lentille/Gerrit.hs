{-# LANGUAGE FlexibleContexts #-}

-- |
-- Copyright: (c) 2021 Monocle authors
-- SPDX-License-Identifier: AGPL-3.0-only
-- Maintainer: Monocle authors
--
-- Monocle Gerrit crawler system
module Lentille.Gerrit
  ( streamProject,
    streamChange,
    G.GerritProjectQuery (..),
    G.GerritQuery (..),

    -- * The context
    MonadGerrit,
    runGerritM,
  )
where

import Control.Monad.IO.Unlift
import qualified Data.Attoparsec.Text as P
import Data.Char
import qualified Data.Map as M (elems, keys, lookup, toList)
import qualified Data.Text as T
import qualified Data.Vector as V
-- import Gerrit hiding (changeUrl)
import qualified Gerrit as G
import Gerrit.Data.Change
import Gerrit.Data.Project (GerritProjectInfo (gerritprojectinfoId), GerritProjectsMessage)
import qualified Google.Protobuf.Timestamp as T
import Lentille
import Lentille.GitLab.Adapter (diffTime, fromIntToInt32, getChangeId, ghostIdent, toIdent)
import Monocle.Backend.Documents (docTypeToText)
import Monocle.Backend.Index (getEventType)
import qualified Monocle.Change as C
import Monocle.Prelude (MonadCatch, MonadMask, MonadThrow, hoist)
import qualified Monocle.Project as P
import qualified Network.URI as URI
import Proto3.Suite (Enumerated (..))
import Relude hiding (all, id)
import qualified Streaming.Prelude as S
import Prelude (last)

-------------------------------------------------------------------------------
-- Gerrit context
-------------------------------------------------------------------------------

-- | A newtype for the GerritClient Reader
newtype GerritM a = GerritM (ReaderT G.GerritClient LentilleM a)
  deriving newtype (Functor, Applicative, Monad, MonadIO, MonadCatch, MonadThrow, MonadMask)
  deriving newtype (MonadReader G.GerritClient)

-- | Helper to run a GerritM in IO
runGerritM :: G.GerritClient -> GerritM a -> IO a
runGerritM client (GerritM im) = do
  res <- runLentilleM $ runReaderT im client
  case res of
    Left e -> error (show e)
    Right r -> pure r

-- | A type class for the Gerrit API
class (Monad m, MonadReader G.GerritClient m) => MonadGerrit m where
  getProjects :: Int -> G.GerritProjectQuery -> Maybe Int -> m GerritProjectsMessage
  queryChanges :: Int -> [GerritQuery] -> Maybe Int -> m [GerritChange]

-- | The MonadGerrit instance using the concret reader
instance MonadGerrit GerritM where
  getProjects count query startM = do
    client <- ask
    liftIO $ G.getProjects count query startM client
  queryChanges count queries startM = do
    client <- ask
    liftIO $ G.queryChanges count queries startM client

-- | The MonadLog instance for logging
instance MonadLog GerritM where
  log' = liftIO . logEvent

-- | The MonadRetry instance for retrying
instance MonadRetry GerritM where
  retry = retry'

-------------------------------------------------------------------------------
-- Monocle Gerrit crawler system
-------------------------------------------------------------------------------

-- >>> P.parseOnly approvalsParser "Patch Set 10: Code-Review+2 Workflow+1"
-- Right ["Code-Review+2","Workflow+1"]
-- >>> P.parseOnly approvalsParser "Patch Set 1:\n\nStarting check jobs."
-- Left "string"
-- >>> P.parseOnly approvalsParser "Patch Set 3: Verified-1\n\nBuild failed."
-- Right ["Verified-1"]
approvalsParser :: P.Parser [Text]
approvalsParser = do
  void $ P.string "Patch Set "
  void (P.decimal :: P.Parser Integer)
  void $ P.string ": "
  word `P.sepBy1` P.char ' '
  where
    word = P.takeWhile1 (not . isSpace)

-- >>> P.parseOnly commentParser "Patch Set 3: Verified-1\n\nBuild failed."
-- Right "Build failed."
-- >>> P.parseOnly commentParser "Patch Set 3: Verified-1"
-- Left "'\\n': not enough input"
commentParser :: P.Parser Text
commentParser = do
  void $ P.takeTill (== '\n')
  void $ P.count 2 $ P.char '\n'
  P.takeText

newPSParser :: P.Parser Text
newPSParser = P.string "Uploaded patch set"

getHostFromURL :: Text -> Text
getHostFromURL url =
  maybe
    (error "Unable to parse provided url")
    (toText . URI.uriRegName)
    (URI.uriAuthority =<< URI.parseURI (toString url))

{-
>>> let v1 = GerritDetailedLabelVote {value = Just 2, account_id = 42}
>>> let v2 = GerritDetailedLabelVote {value = Just 0, account_id = 42}
>>> let v3 = GerritDetailedLabelVote {value = Just (-1), account_id = 42}
>>> let app1 = ("Code-Review", GerritDetailedLabel {all = Just [v1, v2, v3], default_value = 0})
>>> let app2 = ("Verified", GerritDetailedLabel {all = Just [v1, v2, v3], default_value = 0})
>>> toApprovals [app1, app2]
["Code-Review+2","Code-Review-1","Verified+2","Verified-1"]
-}
toApprovals :: [(Text, GerritDetailedLabel)] -> [Text]
toApprovals = concatMap genApprovals
  where
    genApprovals :: (Text, GerritDetailedLabel) -> [Text]
    genApprovals (label, GerritDetailedLabel {..}) =
      (label <>) <$> case all of
        Just votes -> filter (/= "+0") $ genTextVal <$> votes
        Nothing -> []
    genTextVal :: GerritDetailedLabelVote -> Text
    genTextVal vote = case value vote of
      Just v -> if v >= 0 then "+" <> show v else show v
      Nothing -> "+0"

streamProject ::
  (MonadGerrit m, MonadRetry m) =>
  G.GerritProjectQuery ->
  S.Stream (S.Of P.Project) m ()
streamProject query = go 0
  where
    size = 100
    doGet offset = getProjects size query (Just offset)
    go offset = do
      projects <- lift $ do retry . doGet $ offset
      let pNames = gerritprojectinfoId <$> M.elems projects
      S.each $ P.Project . toLazy <$> pNames
      when (length pNames == size) $ go (offset + size)

streamChange ::
  (MonadGerrit m, MonadRetry m) =>
  [GerritQuery] ->
  Maybe Text ->
  S.Stream (S.Of (C.Change, [C.ChangeEvent])) m ()
streamChange query prefixM = do
  client <- ask
  streamChange' client query prefixM

streamChange' ::
  (MonadGerrit m, MonadRetry m) =>
  G.GerritClient ->
  [GerritQuery] ->
  Maybe Text ->
  S.Stream (S.Of (C.Change, [C.ChangeEvent])) m ()
streamChange' client query prefixM = go 0
  where
    size = 100
    go offset = do
      changes <- lift $ do retry . doGet $ offset
      S.each $ (\c -> let cT = toMChange c in (cT, toMEvents cT (messages c))) <$> changes
      when (length changes == size) $ go (offset + size)
    doGet offset = queryChanges size query (Just offset)
    getHost = getHostFromURL $ G.serverUrl client
    prefix = fromMaybe "" prefixM
    getIdent :: GerritAuthor -> C.Ident
    getIdent gAuthor = toIdent getHost Nothing $ toAuthorName (aName gAuthor) (show . aAccountId $ gAuthor)
      where
        toAuthorName name accountID = name <> "/" <> accountID
    toMEvents :: C.Change -> [GerritChangeMessage] -> [C.ChangeEvent]
    toMEvents C.Change {..} messages =
      [toChangeCreatedEvent]
        <> toChangeMergedEvent
        <> toChangeAbandonedEvent
        <> toChangeReviewedEvents
        <> toChangeCommentedEvents
        <> toChangePushedEvents
      where
        baseEvent :: C.ChangeEventType -> C.ChangeEvent
        baseEvent eType =
          let changeEventId = eventTypeToText eType <> changeId
              changeEventCreatedAt = changeCreatedAt
              changeEventAuthor = changeAuthor
              changeEventRepositoryFullname = changeRepositoryFullname
              changeEventRepositoryPrefix = changeRepositoryPrefix
              changeEventRepositoryShortname = changeRepositoryShortname
              changeEventBranch = changeBranch
              changeEventTargetBranch = changeTargetBranch
              changeEventNumber = changeNumber
              changeEventChangeId = changeChangeId
              changeEventUrl = changeUrl
              changeEventOnAuthor = changeAuthor
              changeEventOnCreatedAt = changeCreatedAt
              changeEventChangedFiles = C.ChangedFilePath . C.changedFilePath <$> changeChangedFiles
              changeEventType = Just eType
           in C.ChangeEvent {..}
          where
            eventTypeToText t = docTypeToText . getEventType $ Just t
        toChangeCreatedEvent = baseEvent $ C.ChangeEventTypeChangeCreated C.ChangeCreatedEvent
        toChangeMergedEvent = case changeState of
          Enumerated (Right C.Change_ChangeStateMerged) ->
            [ (baseEvent $ C.ChangeEventTypeChangeMerged C.ChangeMergedEvent)
                { C.changeEventAuthor = case changeOptionalMergedBy of
                    Just (C.ChangeOptionalMergedByMergedBy ident) -> Just ident
                    Nothing -> Nothing,
                  C.changeEventCreatedAt = case changeOptionalMergedAt of
                    Just (C.ChangeOptionalMergedAtMergedAt ts) -> Just ts
                    Nothing -> Nothing
                }
            ]
          _ -> mempty
        toChangeAbandonedEvent = case changeState of
          Enumerated (Right C.Change_ChangeStateClosed) ->
            [ (baseEvent $ C.ChangeEventTypeChangeAbandoned C.ChangeAbandonedEvent)
                { C.changeEventCreatedAt = case changeOptionalClosedAt of
                    Just (C.ChangeOptionalClosedAtClosedAt ts) -> Just ts
                    Nothing -> Nothing
                }
            ]
          _ -> mempty
        toChangeReviewedEvents = mapMaybe toReviewEvent messages
          where
            toReviewEvent GerritChangeMessage {..} = case P.parseOnly approvalsParser mMessage of
              Right approvals ->
                Just $
                  commentBasedEvent
                    (C.ChangeEventTypeChangeReviewed . C.ChangeReviewedEvent $ V.fromList $ toLazy <$> approvals)
                    mAuthor
                    mDate
              Left _ -> Nothing
        toChangeCommentedEvents =
          toCommentBasedEvent commentParser (C.ChangeEventTypeChangeCommented C.ChangeCommentedEvent)
        toChangePushedEvents =
          toCommentBasedEvent newPSParser (C.ChangeEventTypeChangeCommitPushed C.ChangeCommitPushedEvent)
        toCommentBasedEvent parser eType = mapMaybe toEvent messages
          where
            toEvent GerritChangeMessage {..} = case P.parseOnly parser mMessage of
              Right _ ->
                Just $ commentBasedEvent eType mAuthor mDate
              Left _ -> Nothing
        commentBasedEvent t author date =
          (baseEvent t)
            { C.changeEventAuthor = getIdent <$> author,
              C.changeEventCreatedAt = Just . T.fromUTCTime . unGerritTime $ date
            }

    toMChange :: GerritChange -> C.Change
    toMChange GerritChange {..} =
      let changeId = toLazy id
          changeNumber = fromIntToInt32 number
          changeChangeId = getChangeId project (show number)
          changeTitle = toLazy subject
          changeText = getCommitMessage
          changeUrl = toLazy $ G.changeUrl client GerritChange {..}
          changeCommitCount = 1
          changeAdditions = fromIntToInt32 insertions
          changeDeletions = fromIntToInt32 deletions
          changeChangedFilesCount = getFilesCount
          changeChangedFiles = V.fromList getFiles
          changeCommits = V.fromList $ maybe [] getCommits current_revision
          changeRepositoryPrefix = toLazy $ prefix <> T.intercalate "/" (reverse (drop 1 $ reverse $ T.split (== '/') project))
          changeRepositoryFullname =
            if T.null $ toText changeRepositoryPrefix
              then changeRepositoryShortname
              else changeRepositoryPrefix <> "/" <> changeRepositoryShortname
          changeRepositoryShortname = toLazy . Prelude.last $ T.split (== '/') project
          changeAuthor = Just author
          changeOptionalMergedBy =
            if status == MERGED
              then C.ChangeOptionalMergedByMergedBy <$> merger
              else Nothing
          changeBranch = toLazy branch
          changeTargetBranch = toLazy branch
          changeCreatedAt = Just $ toTimestamp created
          changeOptionalMergedAt =
            if status == MERGED
              then Just . C.ChangeOptionalMergedAtMergedAt $ maybe (toTimestamp updated) toTimestamp submitted
              else Nothing
          changeUpdatedAt = Just $ toTimestamp updated
          changeOptionalClosedAt = case status of
            ABANDONED -> Just $ C.ChangeOptionalClosedAtClosedAt $ toTimestamp updated
            MERGED -> Just $ C.ChangeOptionalClosedAtClosedAt $ maybe (toTimestamp updated) toTimestamp submitted
            _ -> Nothing
          changeState = toState status
          changeOptionalDuration =
            C.ChangeOptionalDurationDuration . fromIntToInt32 . diffTime (unGerritTime created)
              <$> (unGerritTime <$> submitted)
          changeMergeable = case mergeable of
            Just True -> "MERGEABLE"
            _ -> "CONFLICT"
          -- Gerrit labels must be handled as Review
          changeLabels = V.fromList []
          -- TODO(fbo) add assignees support to gerrit-haskell
          changeAssignees = V.fromList []
          changeApprovals = V.fromList $ toLazy <$> toApprovals (M.toList labels)
          changeDraft = status == DRAFT
          changeOptionalSelfMerged =
            if status == MERGED
              then C.ChangeOptionalSelfMergedSelfMerged . isSelfMerged owner <$> submitter
              else Nothing
       in C.Change {..}
      where
        getRevision sha = join (M.lookup sha revisions)
        revision = getRevision =<< current_revision
        author = getIdent owner
        uploader = grUploader <$> revision
        merger = getIdent <$> submitter
        isSelfMerged s a = aAccountId s == aAccountId a
        toTimestamp = T.fromUTCTime . unGerritTime
        ghostIdent' = ghostIdent getHost
        getCommitMessage = maybe "" (toLazy . cMessage . grCommit) revision
        getFilesCount = fromIntToInt32 $ maybe 0 (length . M.keys . grFiles) revision
        getFiles = maybe [] (fmap toChangeFile) $ M.toList . grFiles <$> revision
          where
            toChangeFile (fp, details) =
              let changedFileAdditions = maybe 0 fromIntToInt32 $ gfLinesInserted details
                  changedFileDeletions = maybe 0 fromIntToInt32 $ gfLinesDeleted details
                  changedFilePath = toLazy fp
               in C.ChangedFile {..}
        getCommits sha = maybe [] toCommit $ grCommit <$> revision
          where
            toCommit GerritCommit {..} =
              -- TODO(fbo) ensure alias callback is passed
              let commitSha = toLazy sha
                  commitAuthor = Just author
                  commitCommitter = Just $ maybe ghostIdent' getIdent uploader
                  commitAuthoredAt = Just . T.fromUTCTime . unGerritTime . caDate $ cAuthor
                  commitCommittedAt = Just . T.fromUTCTime . unGerritTime . caDate $ cCommitter
                  commitAdditions = fromIntToInt32 insertions
                  commitDeletions = fromIntToInt32 deletions
                  commitTitle = toLazy cSubject
               in [C.Commit {..}]
        toState :: GerritChangeStatus -> Enumerated C.Change_ChangeState
        toState = \case
          ABANDONED -> Enumerated (Right C.Change_ChangeStateClosed)
          MERGED -> Enumerated $ Right C.Change_ChangeStateMerged
          NEW -> Enumerated $ Right C.Change_ChangeStateOpen
          DRAFT -> Enumerated $ Right C.Change_ChangeStateOpen

-- Helper to convert a BugzillaM into a LentilleM
toLentilleM :: G.GerritClient -> GerritM a -> LentilleM a
toLentilleM client (GerritM im) = runReaderT im client

-- | The LentilleM adapter, which takes care of converting the `MonadGerrit m => Stream (Of P.Project) m ()`
--   into a `Stream (Of P.Project) LentilleM ()` using mmorph hoist favility.
_getProjectsStream ::
  G.GerritClient ->
  G.GerritProjectQuery ->
  S.Stream (S.Of P.Project) LentilleM ()
_getProjectsStream client query = hoist (toLentilleM client) $ streamProject query

-- | The LentilleM adapter, which takes care of converting the `MonadGerrit m => Stream (Of (C.Change, [C.ChangeEvents])) m ()`
--   into a `Stream (Of (C.Change, [C.ChangeEvent])) LentilleM ()` using mmorph hoist favility.
_getChangesStream ::
  G.GerritClient ->
  [G.GerritQuery] ->
  Maybe Text ->
  S.Stream (S.Of (C.Change, [C.ChangeEvent])) LentilleM ()
_getChangesStream client queries prefixM = hoist (toLentilleM client) $ streamChange queries prefixM