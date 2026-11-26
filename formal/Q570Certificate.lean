import Std

/-! Algebra and pathwise betting calculations for the four-point certificate.
    Probabilities, independence, integration and almost-sure identities are
    treated in the accompanying paper. -/
namespace MergerWitness
open Lean.Grind

def merger {R : Type} [CommRing R] (x y z a b c : R) : R :=
  1 + (x-1)*((1-b)*c) + (y-1)*((1-c)*a) + (z-1)*((1-a)*b)

theorem remainderIdentity {R : Type} [CommRing R] (a b c : R) :
    1 - ((1-b)*c + (1-c)*a + (1-a)*b) = a*b*c + (1-a)*(1-b)*(1-c) := by grind

theorem fourValues :
    merger (1/4 : Rat) (1/4) (1/4) 0 0 0 = 1 ∧
    merger (0 : Rat) (1/4) (3/4) 0 0 1 = 0 ∧
    merger (3/4 : Rat) 0 (1/4) 1 0 0 = 0 ∧
    merger (1/4 : Rat) (3/4) 0 0 1 0 = 0 := by decide +kernel

def bet (s x : Rat) : Rat := 1-s+s*x

theorem smallBound (s : Rat) (h : 0 ≤ s) (h' : s ≤ 1) :
    0 ≤ bet s (1/4) ∧ bet s (1/4) ≤ 1 := by unfold bet; grind

theorem firstWagerZero (s : Rat) (h : 0 ≤ s) (endWealth : Rat)
    (hcap : endWealth ≤ bet s (1/4)) (hsat : 1 ≤ endWealth) : s = 0 := by
  unfold bet at hcap
  grind

theorem positiveFactor (s x : Rat) (hs : 0 ≤ s) (ht : s ≤ 1) (hx : 0 < x) :
    0 < bet s x := by
  unfold bet
  by_cases he : s = 0
  · subst s; simp; decide +kernel
  · have hpos : 0 < s := by grind
    have hp : 0 < s*x := Rat.mul_pos hpos hx
    grind

theorem survivesZeroFirst (s t x y : Rat) (hs : 0 ≤ s) (hs' : s ≤ 1)
    (ht : 0 ≤ t) (ht' : t ≤ 1) (hx : 0 < x) (hy : 0 < y) :
    0 < bet 0 0 * bet s x * bet t y := by
  have h := Rat.mul_pos (positiveFactor s x hs hs' hx) (positiveFactor t y ht ht' hy)
  have hz : bet 0 0 = 1 := by decide +kernel
  rw [hz, Rat.one_mul]
  exact h

theorem quantitativeGap (mA m1 m2 m3 err : Rat)
    (h : mA ≤ 1/4 + 4*(m1+m2+m3)) (ha : 1-err ≤ mA)
    (h1 : m1 ≤ err) (h2 : m2 ≤ err) (h3 : m3 ≤ err) : 3/52 ≤ err := by grind

#print axioms quantitativeGap
#print axioms remainderIdentity
#print axioms fourValues
#print axioms smallBound
#print axioms firstWagerZero
#print axioms positiveFactor
#print axioms survivesZeroFirst
end MergerWitness
