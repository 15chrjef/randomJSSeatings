#!/usr/bin/env Node

function makeGroups (){
	var num = Number(process.argv[2]);
	var kids = process.argv[3].split(',').map(Number);
	var iterations = Math.floor(kids.length/num)
	var groupsArr = [];
	var groupVals = [];
	for(var x = 0; x < num; x++){
		groupsArr.push([])
		groupVals.push(0)
	}

	var divisible = num % 2 === 0? true: false;
	for(var i = 0, length = kids.length/2; i < length; i++){
		var groupToPush = i % num
		if(kids.length >= 2* num + 2 || divisible){
			var highLow = findHighLow()
			var low = kids.shift()
			var high = kids.pop()
			groupsArr[groupToPush].push(low)
			groupsArr[groupToPush].push(high)
		} 
		console.log('kids', kids)
	}
	if(kids.length > 0){
		for(var j = i % num, length = kids.length; j <= length; j++){
			var groupToPush = j % num
			var low = kids.shift()
			groupsArr[groupToPush].push(low)
		}
	}
	for(var y = 0; y < groupsArr.length; y++){
		console.log(groupsArr[y].join(' '))
	}
}

makeGroups()