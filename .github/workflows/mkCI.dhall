-- Re-usable github action for cachix
let GithubActions =
      https://raw.githubusercontent.com/regadas/github-actions-dhall/afa8b8dad361f795ddd24e6d5c54b23e57bca623/package.dhall
        sha256:98ee16e6add21cc8ea7804cce55793b8793b14479f248d8f0bda0209d3600e18

in  { GithubActions
    , elastic-steps =
      [ GithubActions.Step::{
        , name = Some "Configure sysctl limits"
        , run = Some
            ''
            sudo swapoff -a
            sudo sysctl -w vm.swappiness=1
            sudo sysctl -w fs.file-max=262144
            sudo sysctl -w vm.max_map_count=262144
            ''
        }
      , GithubActions.Step::{
        , name = Some "Runs Elasticsearch"
        , uses = Some "elastic/elastic-github-actions/elasticsearch@master"
        , `with` = Some (toMap { stack-version = "7.8.0" })
        }
      , GithubActions.Step::{
        , name = Some "Display indexes"
        , run = Some "curl -s -I -X GET http://localhost:9200/_cat/indices"
        }
      ]
    , makeNix =
        \(cache-name : Text) ->
        \(steps : List GithubActions.Step.Type) ->
          let boot =
                \(name : Text) ->
                  [ GithubActions.Step::{
                    , uses = Some "actions/checkout@v2.4.0"
                    , `with` = Some (toMap { submodules = "true" })
                    }
                  , GithubActions.Step::{
                    , uses = Some "cachix/install-nix-action@v15"
                    , `with` = Some
                        (toMap { nix_path = "nixpkgs=channel:nixos-unstable" })
                    }
                  , GithubActions.Step::{
                    , uses = Some "cachix/cachix-action@v10"
                    , `with` = Some
                        ( toMap
                            { name
                            , authToken = "\${{ secrets.CACHIX_AUTH_TOKEN }}"
                            }
                        )
                    }
                  ]

          in  GithubActions.Workflow::{
              , name = "Nix"
              , on = GithubActions.On::{
                , pull_request = Some GithubActions.PullRequest::{=}
                , push = Some GithubActions.Push::{=}
                , release = Some GithubActions.Release::{=}
                }
              , jobs = toMap
                  { tests = GithubActions.Job::{
                    , name = Some "tests"
                    , runs-on = GithubActions.RunsOn.Type.ubuntu-latest
                    , steps = boot cache-name # steps
                    }
                  }
              }
    , makeNPM =
        \(steps : List GithubActions.Step.Type) ->
          let init =
                [ GithubActions.Step::{ uses = Some "actions/checkout@v2.4.0" }
                , GithubActions.Step::{
                  , uses = Some "actions/setup-node@v2"
                  , `with` = Some (toMap { node-version = "16" })
                  }
                ]

          in  GithubActions.Workflow::{
              , name = "Web"
              , on = GithubActions.On::{
                , pull_request = Some GithubActions.PullRequest::{=}
                , push = Some GithubActions.Push::{=}
                , release = Some GithubActions.Release::{=}
                }
              , jobs = toMap
                  { web-tests = GithubActions.Job::{
                    , name = Some "web-tests"
                    , runs-on = GithubActions.RunsOn.Type.ubuntu-latest
                    , steps = init # steps
                    }
                  }
              }
    , makeCompose =
        \(steps : List GithubActions.Step.Type) ->
          let init =
                [ GithubActions.Step::{
                  , uses = Some "actions/checkout@v2.4.0"
                  , `with` = Some (toMap { submodules = "true" })
                  }
                , GithubActions.Step::{
                  , name = Some "Stop provided Docker"
                  , run = Some "sudo systemctl stop docker containerd"
                  }
                , GithubActions.Step::{
                  , name = Some "Remove provided Docker"
                  , run = Some
                      "sudo apt-get remove --autoremove -y moby-engine moby-cli moby-buildx moby-containerd moby-runc"
                  }
                , GithubActions.Step::{
                  , name = Some "Install patched seccomp Docker repository"
                  , run = Some
                      "sudo add-apt-repository -y ppa:pascallj/docker.io-clone3"
                  }
                , GithubActions.Step::{
                  , name = Some "Install patched seccomp Docker"
                  , run = Some "sudo apt-get install -y docker.io"
                  }
                , GithubActions.Step::{
                  , name = Some "Configure sysctl limits"
                  , run = Some
                      "sudo swapoff -a; sudo sysctl -w vm.swappiness=1; sudo sysctl -w fs.file-max=262144; sudo sysctl -w vm.max_map_count=262144"
                  }
                ]

          in  GithubActions.Workflow::{
              , name = "Docker"
              , on = GithubActions.On::{
                , pull_request = Some GithubActions.PullRequest::{=}
                , push = Some GithubActions.Push::{=}
                , release = Some GithubActions.Release::{=}
                }
              , jobs = toMap
                  { compose = GithubActions.Job::{
                    , name = Some "compose-tests"
                    , runs-on = GithubActions.RunsOn.Type.ubuntu-latest
                    , steps = init # steps
                    }
                  }
              }
    }
