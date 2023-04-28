$(document).ready(()=>{
    setTimeout(()=>{
        $("#loadingpage").fadeOut(500);
    }, 1000);
  

    $('.icon-container').click(function(){
        $('.icon-container').removeClass("selected");
        $(this).addClass("selected");
        $('#body').children().hide();
        $(".art").hide()
        $(".big").hide()
        switch($(this).children("p").html()){
            case 'All' :
                $('#body').show();
                $('#body').children().show();
                break;
            case 'Web Dev' :
                $('#body').show();
                $('#body').children('.code').show();
                break;
            case 'ML' :
                $('#body').show();
                $('#body').children('.brain').show();
                break;
            case 'Art' : 
                $('#body').hide();
                $('.art').show();
                break;
            case 'Liked':
                $('#body').show();
                $('#body').children('.liked').show();
        }
    });

    $('.body-icon').children('.fa-heart ').click(function(){
        $(this).parent().parent().toggleClass('liked');
        const id = $(this).parent().parent().attr('id');
        let liked = false;
        $(this).parent().parent().attr('class').includes('liked') ? liked = true : liked = false;
        console.log(liked);
        const data = {
            "liked": liked,
            "id" : id
        }
        const xml = new XMLHttpRequest();
        xml.open("POST",`/likes/${JSON.stringify(data)}`);
        xml.onload = () => {
            var reply = xml.responseText ;
            $(`#${id}`).children('h4').text(reply);
        };
        xml.send();
    });
    
    $('#body').children().children('a').click(function(){
        const id = $(this).parent().attr('id') ;
        const data = {
            "id" : id
        }
        const xml = new XMLHttpRequest();
        xml.open("POST",`/views/${JSON.stringify(data)}`);
        xml.onload = () => {
            var reply = xml.responseText ;
            $(`#${id}`).children('h4').text(reply);
        };
        xml.send();
        window.open(`/article/${id}`,"_self");
    });

    $('.fa-envelope').click(function(){
        $('#form').css('display','flex');
        $('#layer').css('display','block');
    });

    $('#close').click(function(){
        $('#form').css('display','none');
        $('#layer').css('display','none');
    });

    $('#layer').click(function(){
        $('#form').css('display','none');
        $('#layer').css('display','none');
    })

    $("#form").submit(function(e) {
        e.preventDefault();
        $.ajax({
          type:'POST',
          url:'/',
          data:{
            email:$("#email").val(),
            message:$("#message").val()
          },
        });
        $('#email').val('');
        $('#message').val('');
    });

    $('#send').click(()=>{
        $('.notification').css('display','flex');
        $('#form').css('display','none');
        $('#layer').css('display','none');

    });

    $('.icon').click(()=>{
        $('.notification').css('display','none');
    });

    $('.close-not').click(()=>{
        $('.notification').css('display','none');
    });

    $('.close-pic').click(function(){
        id = $(this).parent().attr('id');
        console.log(id)
        $(`#${id}.big`).css("display","none");

    });
    $('.piece').click(function(){
        id = $(this).attr('id');
        $(`#${id}.big`).css("display","flex");
    });

});

