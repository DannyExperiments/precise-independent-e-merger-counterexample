# Reproduce the checks

Run the standard-library tests and archive verifier from the repository root.

```sh
python3 -I verification/src/replay.py
python3 -I scripts/verify_repository.py
```

The first command checks both cutoffs at the four witnesses, the Boolean truth table and fractional selector identity at 125 triples. It also checks the expected outputs of finite product laws and the betting inequalities at rational stakes. The proof in the paper applies to arbitrary admissible real stakes and independent input laws.

With a local Lean 4.30.0 installation, run the finite certificate using the standard library.

```sh
lean -DwarningAsError=true formal/Q570Certificate.lean
```

[Exact replay output](verification/logs/replay.txt) · [Lean output](verification/logs/lean.txt) · [Build the manuscript](paper/BUILD.md) · [Visual source](visualization/README.md)
