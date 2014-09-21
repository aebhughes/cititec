cititec
=======

A tech-test passed from an unknow client.

The Task description is described as:
Your	goal	is	to	create	a	program	that	retrieves	data	from	the	Last.fm	service	API	and	provides	the	user	with	information	on	their	listening	habits.

The	script spec:
----------------

- Run	from the command line, receiving the user’s	username as an argument. The Last.FM username assumed)
- Store	data in an easily retrievable format (textfile will be used in this implementation)
- On	each	run	it	should:

  + Retrieve and	store the user’s	track	data	from	the	Last.fm	API.
    - The	most recently listened to tracks not currently stored should be retrieved	first.
    - If	you	still	have remaining	requests (see	limitations),	it should backfill any missing, historically	listened to tracks.
    - You	shouldn't need to do any kind of authentication.	

  +Try	to	produce the	following	information	using	all	data	that	was	just	fetched	as	well	as	all	that	was	previously	stored:
    - Number	of	unique	tracks	listened	to.
    - Top	5 artists	listened	to.
    - Average	number	of	tracks	per	day (excluding	days	with	no	data).
    - Most active day	of the	week by	number of listens.

Example:

`./techtest.py aebhughes
`

Output

`
You have listened to a total of 254 tracks.
Top favourite artists: CCR, Queen, ...
You listen to, on average, 10 tracks a day.
Your most active day is Wednesday'
`
