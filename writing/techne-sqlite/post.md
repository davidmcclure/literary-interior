
# Storing literary feature data in SQLite

A couple weeks ago I wrote about some of the MPI programs we've been running on the campus cluster to pull out features from some of our larger corpora. But - what comes after this? Eventually the cluster job finishes, the processes get killed, the SSD drives get wiped, and the "result" - the data that comes out the far end - has to get flushed to disk in one way or another. What's the best way to store this type of feature data? In a very pragmatic sense - where do you _put_ it?

In the toy example from the last post, this was simple - we were just counting up the total number of words in the Extracted Features data from Hathi, so the result was literally just a single integer, which can just be printed off into the logs at the end of the job. But, in many cases, this "feature" data comes out on the far side can itself be quite large and complex. How to store this, how to warehouse it? Regular text formats like JSON or CSV? Directly serialized data structures like Python's pickles or shelve files? Key-value stores like BekerleyDB, Redis, LevelDB, Rlite, Vedis? Scientific formats like hdf5, via something like PyTables? Tabular formats like Parquet or Avro, from Hadoop-land? Column-based databases like HBase or Cassandra? Or just something no-frills like Postgres or MySQL?

At first this seemed like a fairly workaday programming question - as much a matter of taste, as anything - and I bumbled through a few ideas without really thinking hard about it. But, as I kept trying different things - and running up against unexpected and interesting problems - I realized that this was actually one of those little threads that, when pulled on, ends up unravelling into a set of bigger and more engineering-philosophic questions. It's circular, really - the answer to the technological question of "how to store it?" is really - well, what kind of data is it in the first place? Sitting at the keyboard, working on some particular project, I always had an answer to this in the moment - it's a single integer; it's a set of word counts, broken out by pages that do and don't contain "literature," etc. But, in the general case, this dissolves into the larger normative question - what kind of data _should_ be coming out of these extraction jobs? Should it be big or small, measured in bytes, kilobytes, megabytes, gigabytes? How should it plug in with the process of analysis and interpretation that eventally bakes off the specific little artifacts - values, figures, tables - that get surfaced in pamphlets or articles? How general-purpose or specific should the data be? Should we write programs that produce very flexible and open-ended sets of features that could be used to answer a number of different questions - the first rough cut in a pipeline of steps, a branching tree of analysis that flows into a number of different lines of inquiry - or should the code laser in on one particular question, precipitate out a "finding" in one fell swoop?

To indulge a metaphor that's been used a couple of times in the pamphlets - if we think of ourselves as literary "astronomers" (the corpora are the night sky; the MPI programs on the cluster are like bespoke little radio telescopes that harvest out some kind of observational data about the literary universe) - then, how fine-grained or general-purpose should the observations be? Should we more or less begin with specific, fully-formed hypotheses - presumably flowing from intuitions developed during analog reading experiences, more often than not - and program the telescope to point at one very small little swath of the sky and observe at the specific frequency where we think there might be something of interest? Or should we sweep out big arcs in the night sky - point the telescope in the general direction of the star or galaxy that we've got a hunch about but scoop up lots of data at lots of different frequencies? What's our philosophy of feature extraction, and, in a more general sense, of intellectual _process_ - do we begin with specific literary-critical hypotheses and test them directly, quickly, surgically, or do we begin with a more diffuse critical orientation, listen on a larger range of frequencies, and then let specific lines of inquiry emerge around the salient features that pop out in the process of analysis?

I swing back and forth on this from project to project, I think, and the answer isn't clear to me. Both seem to have risks - start too narrow, and you might miss a more interesting version of the question; start too broad, and you might get lost in a sea of leads and never wrestle things back into contact with literature, as opposed to just language or information in a general sense.

## SQLite

But, back to the pragmatic question of where to put the data - in the last few months I've sort of stumbled into an approach that seemed a little weird at first, but which, as I've gotten further along on a couple of projects, I like more and more - when in doubt, just store everything in SQLite.

This seemed a bit strange, I think, because of some common misconceptions that I had about SQLite from my previous life when I spent most of my time doing application development, not scientific / statistical programming. At first blush SQLite can seem sort of like a toy compared to regular Postgres or MySQL. There's no server - the entire database is stored in a single flat file, and transactions are implemented with unix file locks, which obviously has implications for concurrency that can be showstoppers for, say, a busy web application that needs to do lots of concurrent writes. In my head it was something you might use in mobile apps or embedded systems, for relatively small amounts of data in constrained environments where a full-service database would be overkill.

In fact, though, far from being a toy, SQLite is actually a remarkably, almost dizzyingly serious piece of software. From an engineering perspective, the codebase has acquired a kind of cult following in recent years, and it widely regarded as one of the most sophisticated and robust open-source projects in existence. The testing harness weighs in at a mind-boggling 91 _million_ lines of code, about 800 times larger than the actual application, and covers extreme edge cases that I'd never in a million years think to test - physical power failures, etc. The typing system is a bit eccentric - it's enforced at the level of individual values, not columns, meaning you can store string values in integer columns, for instance - but generally speaking it implements a very complete flavor of the SQL spec. And, far from being limited to small data sets, the database file is happy to grow as large as 140 terabytes, far more than I can ever imagine needing. (The raw data for all of our corpora, by comparison, is just around 5TB.)

And, in fact, many of the things that are often cited as problems or limitations with SQLite actually turn out to be advantages in the context scientific / cluster computing. For example, the fact that it's server-less, just a C program that gets embedded inside of an application, not a separate service that communicates over the network - this means that it can be used in HPC environments where it's difficult or impossible to create daemonized services - it's no different from just dumping data into a pickle or JSON file. And, from a standpoint of research methods, the minimalistic flat-file ethos is really attractive. The file can be put under version control with something like Git LFS, uploaded to Dropbox and shared with colleagues, or dropped into an institutional repository. No need to fiddle with deployments or configuration, bake off SQL dumps, etc. - the database and the data are just one-in-the-same. And, because SQLite is so ubiquitous, and bindings exist onto it from essentially all languages - it's not too far outside the the pantheon of canonical unix utilities like grep or awk - it's almost as portable as a text format like JSON or CSV.

# The literary interior

But, by far the biggest advantage is the flexibility that something like SQLite provides during analysis. To take an example - recently I've been writing some code that looks at the the distribution of words inside of a collection of about 30,000 19th and 20th century novels. The idea is to take a systematic look at the internal structure of long narratives - the ways that plot, theme, syntax, and meaning distribute in different regions of texts. There have been a couple of really interesting projects in the last few years that have looked at specific angles onto this. Most well-known is probably Matt Jockers' "Syuzhet," which plots the movement of "sentiment" across narrative time; in the inagural edition of Cultural Analytics, Andrew Piper builds a computational model of the conversion narrative, typified by the Confessions marked by a semantic swerve near the end, and then uses this signature to find other "conversaional" texts; Ben Schmidt looked at the distribution of topics inside of TV scripts, and was able to tease out a snapshot of the prototypical cop drama, a crime at the beginning and a trial ad the end; here in the Lab, the Suspense project is plotting out the movement of suspense and un-suspense across novels, and Holst Katsma looked at changes in the level of "loudness" across the text. And, in computational linguistics, there's an older and well-established line of work on this general question (though with a more applied than critical bent), dating back to Marti Hearst's work in the last 80s on text segmentation.

Building on this - what could be learned by taking a lower-level, sort of "basic science" approach to the question? Instead of starting with a specific phenomenon - sentiment, loudness, suspense - what could be learned just be looking at the distributions of individual words inside of texts, but at a really large and comprehensive scale? What patterns would emerge? What do beginnings, middles, and ends actually consist of, considered at the scale of many tens or hundreds of thousands of nvoels? Do these textual "regions" have consistent thematic signatures, or does it all wash out in the aggregate? To take up a question posed recently in a collection of essays called _Narrative Middles_, edited by Caroline Levine and Mario Ortiz-Robles - what is a "middle," exactly? Is it just a matter of what it's not - not the beginning, not the end, the connective tissue in between - or is it conceptually addressable region in a text, something with a consistent signature across many novels? And, if these narrative regions do instantiate in computationally observable ways - how stable are they over time? Have the archetypal metaphors for narrative structure - a day, a life, a season, a courtship, a marriage - changed over time? Are beginnings, middles, ends, climaxes, denouements different in 1940 than in 1900, or 1860, 1820, etc? What's the _shape_ of narrative, present and past?

Here's the SQLite schema I'm using:

```sql
CREATE TABLE token (
	corpus VARCHAR NOT NULL,
	year INTEGER NOT NULL,
	token VARCHAR NOT NULL,
	pos VARCHAR NOT NULL,
	"offset" INTEGER NOT NULL,
	count INTEGER NOT NULL,
	PRIMARY KEY (corpus, year, token, pos, "offset")
);
```

Where "offset" is a 0-100 integer that represents a percentile along the X-axis inside of the texts. For example, these rows:

```
gail|1900|the|DT|14|136894
gail|1900|the|DT|15|136880
gail|1900|the|DT|16|136213
```

Mean that the word "the" appeared 136,894 times in the Gail American Fiction corpus, in years between 1895 and 1904, as a determiner, and at the 14% marker in narrative time. At the 15% marker, 136,880 times; at 16%, 136,213 times, and so on and so forth.

When this table is indexed with all ~20k novels in the Gail corpus (roughly 1820 - 1920) and another ~10k novels from the 20th century, the counts get broken out into 132,700,715 rows, which SQLite packs into a (fairly) economical 9.2g file. Indexes are left off, by default, to speed up the bulk-insertion that happens during the final step in the extraction pipeline, but, once the table is loaded, indexes can be added to the individual columns to speed up queries:

```sql
CREATE INDEX token_corpus on token(corpus);
CREATE INDEX token_year on token(year);
CREATE INDEX token_token on token(token);
CREATE INDEX token_pos on token(pos);
CREATE INDEX token_offset on token(offset);
```

Now, with the table loaded and indexed, it's trivial to query out time-series trends for any combination of words, years, parts of speech, or corpora. For example, to get a (narrative) time-series for an individual word, in both corpora and across all years, we can just filter on the token, group by offset, and sum up the counts:

```sql
SELECT offset, SUM(count)
FROM token
WHERE token="young"
GROUP BY offset
ORDER BY offset;
```

Just as a gut check on the method, here at the trends for a couple words we'd expect to mark beginnings:

![](single/young.png)

![](single/boy.png)

![](single/girl.png)

![](single/school.png)

And, ends:

![](single/death.png)

![](single/victory.png)

![](single/defeat.png)

![](single/embrace.png)

Looks about right. Are these trends consistent between the two corpora, separated by about a century? We can slice them apart just by tacking on another `WHERE` clause:

```sql
-- Offsets for "young," just in Gail:
SELECT offset, SUM(count)
FROM token
WHERE token="young" AND corpus="gail"
GROUP BY offset
ORDER BY offset;

-- And, just in Chicago:
SELECT offset, SUM(count)
FROM token
WHERE token="young" AND corpus="chicago"
GROUP BY offset
ORDER BY offset;
```

![](split/young.png)

![](split/boy.png)

![](split/girl.png)

![](split/school.png)

![](split/death.png)

![](split/victory.png)

![](split/defeat.png)

![](split/embrace.png)

Very similar. In other cases, though, there are interesting differences - words related to marriage shift towards the narrative beginning, somewhere in the space between the Gail and Chicago corpora:

![](split/marriage.png)

So, marriage increasingly becomes the _subject_ of narrative, not just its endpoint. Beyond words like these that have pretty obvious narratalogical anchorings, though - even function words that don't carry any kind of semantic meaning show really pronounced trends. Here's "the," again broken out for Gail and Chicago:

![](split/the.png)

This starts to edge in a more interesting direction, I think. In a way, it's a bit remarkable that there's _any_ effect here, let alone something so significant - the null hypothesis is that everything would wash out into a uniform distribution, a flat line, that there would be no relationship between the frequency of a word and its position in the narrative. But, "the" - the most common word in the language - has a highly irregular trend, with huge statistical significance (the chi-square p-value literally rounds down to 0, when printed out in Python). So - beginnings and ends are "concrete," in some sense, preoccupied with specific, definite objects? This makes sense. At the start - the stage has to be set, the scene filled with props and characters, the fictional world populated with matter; at the end - the action of the text has to climax and resolve, the plot has to move into its final pose, the pieces moved into their endgame positions. Beginnings and ends are preoccupied with narrative _stagecraft_, which, it seems, pulls the narrative register outwards into the external world and pins it onto specific places and things - the chair, the table, the house, the city, the countryside, the car, the train, the gun, the wedding, the deathbed, etc.

Unlike with the more semantically focused words, this also starts to feel like a keyhole view onto some kind of broad narratalogical skeleton, a set of structural priors baked into the DNA of stories that manifest in consistent ways across narrative time in large numbers of texts. But, as is often the case at this distance, it's epistemologically difficult - what can be said, at a literary register, about the the "boundaries" that seem to get marked off by this? Do the peaks at the beginning and the end mark _the_ beginning and end - does the beginning end at right around the 20% mark, and the end begin right around 65-70%, when it begins to tick back up? If so - why? What would this actually mean, how to interpret it? Is this novelistic convention, essentially, or is there some sense in which it _must_ be this way, that it would be nearly impossible to write a novel that doesn't show this pattern? And what exactly does one of these phase shifts consist of, on the forest floor of an individual text? When the narrative moves out of the concrete beginning - what does it move _into_? What's just across the threshold, in the beginning of the middle, how is 25% different from 20%? It's a zero-sum game - something has to take the place of "the" (and whatever larger semantic cohort it's likely proxying), but what?

Other things are weirder. Check out the present tenses of "to be":

![](split/is.png)
![](split/are.png)

And the past tenses, which are essentially mirror images:

![](split/was.png)
![](split/were.png)

This seems like a possible window onto the temporal orientation or "direction" of the text, whether the what's being narrated happened now or in the past. So, it seems like "presentness" starts low, peaks out in the middle, dips down in the third quarter, and then spikes up massively at the very end? And conversely, "pastness" is highest at the beginning, declines through the middle, bumps up, and then plummets at the very end?

Or, to end on a head-scratcher, also related to the temporality of the grammar - check out "had," which, between the Gail and Chicago corpora, sloshes from the end to the beginning:

![](split/had.png)

In C20 - narratives begin in the past perfect?

Anyway, the point being - once the data is structured this way, it's easy to answer a whole _class_ of related questions, not just the one or two that I started out with. To circle back to the original question of what type of data should flow out of the cluster, whether it should be big or small, general-purpose or specific - SQLite sort of lets you have the cake and eat it too. It's possible to write code that dragnets out really quite large large amounts of data that answer the question at hand in the most general and comprehensive case, but then plug the resulting data set - tens, even hundreds of gigabytes - directly into a Jupyter notebook and start answering specific questions immediately. It's a nice glue between the process of observation and analysis, between the huge telescope that vacuums up data out of the sky and the little workstation where you sit down and actually figure stuff out.
