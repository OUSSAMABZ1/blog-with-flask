$(document).ready(()=>{
    $('.article-btn').click(function(){
        const id = $(this).attr('id');
        const data = {
            "type" : 'article',
            "id" : id
        }
        const xml = new XMLHttpRequest();
        xml.open("POST",`/delete/${JSON.stringify(data)}`);
        xml.send();
    });
    $('.message-btn').click(function(){
        const id = $(this).attr('id');
        const data = {
            "type" : 'message',
            "id" : id
        }
        const xml = new XMLHttpRequest();
        xml.open("POST",`/delete/${JSON.stringify(data)}`);
        xml.send();
    });
});