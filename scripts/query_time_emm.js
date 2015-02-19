db.test.aggregate([{$project:{day:{$dayOfMonth:'$time'},month:{$month:'$time'},year:{$year:'$time'}}},
{$group:{_id:{day:'$day',month:'$month',year:'$year'}, count: {$sum:1}}}])