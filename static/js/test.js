var audio = $("#wordAudio")[0];
var beepAudio = $("#beepAudio")[0];
var prevBtn = $('#prevBtn');
var nextBtn = $('#nextBtn');
var answers = new Array($('#answer1'), $('#answer2'), $('#answer3'), $('#answer4'));
var queIndex = $('.circle');
var cur = 0;
var total=data.length;


function playAudio(){
    audio.play();
}

function select(index) {
    console.log(index);
    data[cur].answer = index;
    for (i = 0; i < 4; i++){
        if (i == index){
            answers[i].addClass('selected');
        }
        else{
            answers[i].removeClass('selected');
        }
    }
    beepAudio.play();
}

function update(){
    console.log('cur item is:' + cur);
    if (cur == 0) {
        prevBtn.addClass('disabled');
    } else {
        prevBtn.removeClass('disabled');
    }
    if (cur < total - 1 && total > 1) {
        nextBtn.removeClass('disabled');
    } else {
        nextBtn.addClass('disabled');
    }
    $(".circle").each(function(index, element) {
		var index = $(this).text();
		if (cur == index - 1){
		    $(this).removeClass('blue');
		    $(this).addClass('orange');
		} else {
		    $(this).css(" background-color", '#29b6f6'); // blue
		    $(this).removeClass('orange');
		    $(this).addClass('blue');
		}
    });

    audio.pause();
    audio.src = data[cur].audio;
    $('#word').text(data[cur].word);
    for (var i = 0; i < 4; i++){
        answers[i].attr('src', data[cur].images.images[i])
        answers[i].removeClass('selected');
        if (i == data[cur].answer)
            answers[i].addClass('selected');
    }
    audio.play();
}

function prevItem(){
    if (cur > 0){
        cur -= 1;
        update();
    }
}

function nextItem(){
    if (cur < total - 1){
        cur += 1;
        update();
    }
}

function selItem(index) {
    console.log('Item select:' + index)
    cur = index - 1;
    update();
}

function submit() {
}

update();
window.onbeforeunload = function() {
　　return "确定离开页面吗？";
}