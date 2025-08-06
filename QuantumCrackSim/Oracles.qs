namespace Quantum.Oracles {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Preparation;

    /// # Operation: CheckPasswordOracle
    /// Oráculo cuántico que marca una combinación de bits que representa una "contraseña" correcta.
    /// Aquí simulamos que la contraseña correcta es un valor conocido (ej: "1011").
    ///
    /// ## Entradas:
    /// - `candidateKey`: qubits que representan la clave candidata (en binario).
    /// - `target`: qubit auxiliar que se voltea si el candidato es correcto (efecto de fase si se usa con phase kickback).
    ///
    /// ## Nota:
    /// Este oráculo compara el estado cuántico con un valor clásico predefinido.
    operation CheckPasswordOracle(
        candidateKey: LittleEndian,
        target: Qubit
    ) : Unit is Adj + Ctl {
        let desiredKey = [true, false, true, true]; // Representa "1011" (clave correcta: 11 en decimal)
        using (register = Qubit[Length(desiredKey)]) {
            let regLE = LittleEndian(register);

            // Convertir desiredKey (lista de bools) a estado cuántico |desiredKey⟩
            ApplyZipWithCA(CNOT, desiredKey, register);

            // Comparar: si candidateKey == desiredKey, aplicar X al target
            within {
                // Restar desiredKey de candidateKey → resultado cero si son iguales
                SubtractI(regLE, candidateKey);
            } apply {
                // Si la diferencia es cero, candidateKey == desiredKey
                X(target);
                (Controlled OnFixedPoint(Zero))(candidateKey!, target);
                X(target);
            }

            // Deshacer la resta
            // (automático en `within...apply`)
        }
    }

    /// # Operation: RunGroverOracle
    /// Ejemplo de cómo usar el oráculo (para pruebas clásicas o simulación).
    operation RunGroverOracle(keyBits: Bool[]) : Result {
        // Convertir entrada clásica a qubits
        using ((qubits, target) = (Qubit[Length(keyBits)], Qubit())) {
            let candidate = LittleEndian(qubits);

            // Preparar estado |keyBits⟩
            for i in 0..Length(keyBits)-1 {
                if keyBits[i] {
                    X(qubits[i]);
                }
            }

            // Aplicar oráculo
            CheckPasswordOracle(candidate, target);

            // Medir si fue marcado
            let result = MResetZ(target);

            // Resetear qubits
            ResetAll(qubits);

            return result;
        }
    }
}

namespace Quantum.Oracles {
    operation CheckPassword(InputHash : String) : Result {
        // Aquí iría el código del oráculo que verifica si una clave coincide con el hash

        Message($"🔎 Revisando hash: {InputHash}");
        return Zero;
    }
}

