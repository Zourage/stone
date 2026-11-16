## D04 — Scientific argument, 1859

To suppose that the eye, with all its inimitable contrivances for adjusting the focus to different distances, for admitting different amounts of light, and for the correction of spherical and chromatic aberration, could have been formed by natural selection, seems, I freely confess, absurd in the highest possible degree. Yet reason tells me, that if numerous gradations from a perfect and complex eye to one very imperfect and simple, each grade being useful to its possessor, can be shown to exist; if further, the eye does vary ever so slightly, and the variations be inherited, which is certainly the case; and if any variation or modification in the organ be ever useful to an animal under changing conditions of life, then the difficulty of believing that a perfect and complex eye could be formed by natural selection, though insuperable by our imagination, can hardly be considered real.

## D08 — Recipe, 1861

Mode.--As a ham for baking should be well soaked, let it remain in water for at least 12 hours. Wipe it dry, trim away any rusty places underneath, and cover it with a common crust, taking care that this is of sufficient thickness all over to keep the gravy in. Place it in a moderately-heated oven, and bake for nearly 4 hours. Take off the crust, and skin, and cover with raspings, the same as for boiled ham, and garnish the knuckle with a paper frill. This method of cooking a ham is, by many persons, considered far superior to boiling it, as it cuts fuller of gravy and has a finer flavour, besides keeping a much longer time good.

## D12 — Programming documentation

The try statement works as follows.
 First, the try clause (the statement(s) between the try and except keywords) is executed. If no exception occurs, the except clause is skipped and execution of the try statement is finished. If an exception occurs during execution of the try clause, the rest of the clause is skipped.  Then, if its type matches the exception named after the except keyword, the except clause is executed, and then execution continues after the try/except block. If an exception occurs which does not match the exception named in the except clause, it is passed on to outer try statements; if no handler is found, it is an unhandled exception and execution stops with an error message.

## D16 — Programming question with code

Title: What does the "yield" keyword do in Python?
What functionality does the yield keyword in Python provide?
For example, I'm trying to understand this code1:
def _get_child_candidates(self, distance, min_dist, max_dist):
    if self._leftchild and distance - max_dist < self._median:
        yield self._leftchild
    if self._rightchild and distance + max_dist >= self._median:
        yield self._rightchild  

And this is the caller:
result, candidates = [], [self]
while candidates:
    node = candidates.pop()
    distance = node._get_dist(obj)
    if distance <

## D20 — Weather forecast discussion

A deep upper low in the NE Pacific dives southwards well offshore on Wednesday. The bulk of the energy associated with this system will be focused south of western Washington as the system moves onshore into California on Thursday. Precipitation spreads northwards into Washington on Wednesday, however, POPs mainly remain confined south of Seattle, and especially south of WA/OR border due to the trajectory of the system. Easterly winds increase in the Cascade Valleys and gaps early Wednesday for breezy conditions, with NBM probabilities of gusts over 30 MPH in areas around North Bend and Enumclaw around 30-60%. Drier conditions by Thursday into Friday. Periods of clearing may result in fog development, mainly Friday AM. Ensembles suggest troughing deepens again offshore Saturday into next week, with some uncertainty into the exact positioning and depth of the trough. Highs remain near normal during this period in upper 40s to low 50s.

## D24 — Mathematical proof (standard argument, worded for this test)

Theorem. There are infinitely many prime numbers.
Proof. Suppose, for contradiction, that there are only finitely many primes, and call them p1, p2, ..., pn. Let N = p1 p2 ... pn + 1. Since N > 1, some prime q divides N. But q cannot be any of p1, ..., pn, because dividing N by any pi leaves remainder 1. So q is a prime not on our list, contradicting the assumption that the list was complete. Hence there are infinitely many primes.

