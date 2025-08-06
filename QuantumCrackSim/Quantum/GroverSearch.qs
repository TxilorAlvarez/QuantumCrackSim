namespace GroverSearch {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Convert;

    operation SearchPassword(match : Int[], iterations : Int) : Int {
        let nQubits = Length(match);
        use qubits = Qubit[nQubits];

        // Step 1: Superposition
        ApplyToEach(H, qubits);

        // Step 2: Oracle
        operation Oracle(pattern : Int[], qs : Qubit[]) : Unit is Adj + Ctl {
            for (i in IndexRange(qs)) {
                if (pattern[i] == 0) {
                    X(qs[i]);
                }
            }

            if (Length(qs) > 1) {
                Controlled Z(qs[0..nQubits - 2], qs[nQubits - 1]);
            } else {
                Z(qs[0]);
            }

            for (i in IndexRange(qs)) {
                if (pattern[i] == 0) {
                    X(qs[i]);
                }
            }
        }

        // Step 3: Diffusion
        operation Diffusion(qs : Qubit[]) : Unit is Adj + Ctl {
            ApplyToEach(H, qs);
            ApplyToEach(X, qs);

            if (Length(qs) > 1) {
                Controlled Z(qs[0..nQubits - 2], qs[nQubits - 1]);
            } else {
                Z(qs[0]);
            }

            ApplyToEach(X, qs);
            ApplyToEach(H, qs);
        }

        // Step 4: Iteration Loop
        for (i in 1..iterations) {
            Oracle(match, qubits);
            Diffusion(qubits);
        }

        // Step 5: Measurement
        mutable results = new Result[nQubits];
        for (i in IndexRange(qubits)) {
            set results w/= i <- MResetZ(qubits[i]);
        }

        return ResultArrayAsInt(results);
    }

    function ResultArrayAsInt(results : Result[]) : Int {
        mutable output = 0;
        for (idx in IndexRange(results)) {
            if (results[idx] == One) {
                set output += 2^idx;
            }
        }
        return output;
    }
}
