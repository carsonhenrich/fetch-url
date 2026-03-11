{
  description = "A Python script to fetch url page titles and content using Selenium";

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
        
        fetch-url = pkgs.writeScriptBin "fetch-url" ''
          #!${pkgs.bash}/bin/bash
          export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
          export PYTHONPATH="$PYTHONPATH:${./.}"
          exec ${pythonEnv}/bin/python ${./fetch_url.py} "$@"
        '';
        
        run-tests = pkgs.writeScriptBin "run-tests" ''
          #!${pkgs.bash}/bin/bash
          export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
          export PYTHONPATH="$PYTHONPATH:${./.}"
          exec ${pythonEnv}/bin/python ${./test_fetch_url.py} "$@"
        '';
        
      in
      {
        packages = {
          default = fetch-url;
          fetch-url = fetch-url;
          tests = run-tests;
        };

        apps = {
          default = {
            type = "app";
            program = "${fetch-url}/bin/fetch-url";
          };
          tests = {
            type = "app";
            program = "${run-tests}/bin/run-tests";
          };
        };

        checks = {
          tests = pkgs.runCommand "fetch-url-tests" {
            buildInputs = [
              pythonEnv
              pkgs.chromium
              pkgs.chromedriver
            ];
          } ''
            export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
            export PYTHONPATH="$PYTHONPATH:${./.}"
            cp ${./fetch_url.py} fetch_url.py
            cp ${./test_fetch_url.py} test_fetch_url.py
            ${pythonEnv}/bin/python test_fetch_url.py
            touch $out
          '';
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.chromium
            pkgs.chromedriver
            fetch-url
            run-tests
          ];
          
          shellHook = ''
            export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
            export PYTHONPATH="$PYTHONPATH:${./.}"
            echo "Selenium environment ready!"
            echo "Run: python fetch_url.py <url>"
            echo "Test: python test_fetch_url.py"
          '';
        };
      }
    );
}
