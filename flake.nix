{
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: {
      defaultPackage = with nixpkgs.legacyPackages.${system};
        writeScriptBin "ttt" ''
          #!${(python3.withPackages (ps: [ ps.pygame ])).interpreter} -OO
          ${builtins.readFile ./main.py}
        '';
    });
}
