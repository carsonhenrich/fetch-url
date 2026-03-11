{
  description = "A Python script to fetch page titles using Selenium";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          selenium
        ]);
        
        fetch-title = pkgs.writeScriptBin "fetch-title" ''
          #!${pkgs.bash}/bin/bash
          export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
          export PYTHONPATH="$PYTHONPATH:${./.}"
          exec ${pythonEnv}/bin/python ${./fetch_title.py} "$@"
        '';
        
        run-tests = pkgs.writeScriptBin "run-tests" ''
          #!${pkgs.bash}/bin/bash
          export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
          export PYTHONPATH="$PYTHONPATH:${./.}"
          exec ${pythonEnv}/bin/python ${./test_fetch_title.py} "$@"
        '';
        
      in
      {
        packages = {
          default = fetch-title;
          fetch-title = fetch-title;
          tests = run-tests;
        };

        apps = {
          default = {
            type = "app";
            program = "${fetch-title}/bin/fetch-title";
          };
          tests = {
            type = "app";
            program = "${run-tests}/bin/run-tests";
          };
        };

        checks = {
          tests = pkgs.runCommand "fetch-title-tests" {
            buildInputs = [
              pythonEnv
              pkgs.chromium
              pkgs.chromedriver
            ];
          } ''
            export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
            export PYTHONPATH="$PYTHONPATH:${./.}"
            cp ${./fetch_title.py} fetch_title.py
            cp ${./test_fetch_title.py} test_fetch_title.py
            ${pythonEnv}/bin/python test_fetch_title.py
            touch $out
          '';
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.chromium
            pkgs.chromedriver
          ];
          
          shellHook = ''
            export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
            export PYTHONPATH="$PYTHONPATH:${./.}"
            echo "Selenium environment ready!"
            echo "Run: python fetch_title.py <url>"
            echo "Test: python test_fetch_title.py"
          '';
        };
      }
    );
}
