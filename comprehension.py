trial = gdf.NITRIFIZIERUNG.apply(lambda x: 'n' if x == 0 else 'j')
trial = [1, 2, 3, 4, 5, 6, 8]
func = [x + x for x in trial]
func = [x for x in trial if x == 5]
func = [x if x == 5 else 'buu' for x in trial]
func
{y: [x*x for x in range(10)] for y in trial}
{y: [x*x for x in range(10)] for y in range(2, 20, 5)}

[[x*x for x in range(10)] for y in range(2, 20, 5)]
