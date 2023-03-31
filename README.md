# volley-stats


## Recorded Meaningful Stats

The following are a set of team wide statistics:
`untouched_balls` : records balls that were missed or untouched without attempting to
determine to which player's zone it corresponded

`four_hits` : records balls

`rotational_fault` : records point lost due to a rotational fault


The following are statistics kept per player:

`missed_serves` : records a missed serve resulting in a serve fault

`unreturned_serves` : records a serve that was not returned by the other team which can
sometimes be considered an Ace. These also include balls that were returned over the net,
but hit out during the serve receive of the opposing team.

`shanked_receives` : records receives that were uncontrollably shanked out of the play area
(outside the court) making it hard if not impossible to recover or receives that might have
stayed in the playing area, but are uncontrollably abrupt to keep in play. If the ball
received is from an opponent spike and the ball is successfully played, it will be
recorded as a `dig` instead

`good_receives` : records receives that keep the ball in play within the vicinity of the
court/playing area

`digs` : records receives from opponent spikes

`bad_pass` : records a bad uncontrolled pass that kills the play when the ball was positioned
in play for a successful pass

`bad_sets` : records a bad uncontrolled set that kills the play or loses attack power when
the ball was positioned in play for a successful set

`doubles` : records double hits by a single player that go over the net. these infractions
are typically called by some of the strictest referees that can spot double hits.

`out_balls` : records ball that were hit out of bounds

`into_net` : records a ball that was hit onto the net when the ball was positioned in play
a successful attack

`kills` : records spikes or kills that result in a point awarded

`blocks` : records successfully blocked balls

`net_touches` : records net touches by a player

`positional_faults` : records positional faults for all players involved in the infraction

`errors` : records uncategorized errors such as a block error/miss that kill the ball from
play and award the opponent a point


```yaml
     detailed: {
      untouched_balls: 0,
      four_hits: 0,
      rotational_fault: 0,

      missed_serves: {},
      unreturned_serves: {},

      shanked_receives: {},
      good_receives: {},
      digs: {},

      bad_pass: {},
      bad_sets: {},
      doubles: {},

      out_balls: {},
      into_net: {},

      kills: {},

      blocks: {},

      net_touches: {},
      positional_faults: {},

      errors: {},
      recoveries: {}
      }
```