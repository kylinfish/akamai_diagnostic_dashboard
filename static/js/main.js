$('body').on('click','.change_speed',function(){
   var clickedBtnID = $(this).closest("tr").find(".telnum").text(); // or var clickedBtnID = this.id
   alert('you clicked on button #' + clickedBtnID);
});