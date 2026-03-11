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
          exec ${pythonEnv}/bin/python ${./fetch_title.py} "$@"
        '';
        
      in
      {
        packages = {
          default = fetch-title;
          fetch-title = fetch-title;
        };

        apps = {
          default = {
            type = "app";
            program = "${fetch-title}/bin/fetch-title";
          };
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.chromium
            pkgs.chromedriver
          ];
          
          shellHook = ''
            export PATH="${pkgs.chromium}/bin:${pkgs.chromedriver}/bin:$PATH"
            echo "Selenium environment ready!"
            echo "Run: python fetch_title.py <url>"
          '';
        };
      }
    );
}
