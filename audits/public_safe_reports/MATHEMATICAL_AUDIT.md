# Mathematical review

The independent review checked that each $w_i$ is independent of $E_i$ under the product law. The weights are nonnegative and their sum is at most one, giving a convex combination and an integrable upper bound. The expectation factors through independence and gives equality whenever each input mean equals one.

At $A$ terminal wealth is at most $c/4+(3/4)c(1-t)$ for initial capital $c$ and first fraction $t$. At $B_i$ every path starting with index $i$ has wealth at least $(3/16)c(1-t)$. These inequalities apply to the same first decision on the different inputs. Integrating yields the four-point inequality and the bound $3/52$. Finite pointwise limits preserve the inequality. Positive mass at a target point in a product law of mean-one marginals provides the known admissibility argument. The evaluation pair $(0,1/4,1/4)$ and $(0,1/4,3/4)$ verifies nonmonotonicity.

The Lean proof checks finite algebra and rational first-wager statements. [Scope](../../STATUS.md) · [Lean certificate](../../formal/Q570Certificate.lean)
