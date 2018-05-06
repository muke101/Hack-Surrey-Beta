$(document).ready(function()
   {

     var selected = [];

     function showLogistics(list)
     {
       var name = list[0]
       var sector = list[1]

       if(name == "Donald Trump")
       {
         $(".text1").text("Donald Trump!!!!!");
         getGraphs(sector);
       }

       else
       {
         $(".text1").text("Type another name, information about " + name+ " not available for now.");
       }


     }

     function getGraphs(sector)
     {

       var image = document.getElementById('graph1');

       if (sector == "Oil")
       {

         image.src = "https://media.istockphoto.com/photos/olive-oil-contained-in-an-round-shaped-bottle-picture-id187205776";

       }

       else if (sector == "Tech")
       {

         image.src = "http://www.cmo.com/content/dam/CMO/Home%20Page/1046x616_Modern-Commerce-2.0-Technology-Sets-The-Stage-For-A-New-Round-Of-Disruption.jpg";

       }

       else if (sector == "CS")
       {

         image.src = "https://media.istockphoto.com/photos/olive-oil-contained-in-an-round-shaped-bottle-picture-id187205776";

       }

       else {
         image.src = "";
       }


    }



    function getValue()
    {

     var name = document.getElementById("nameText").value;
     var sector = document.getElementById("sectorText").value;

     selected = [name,sector];
     showLogistics(selected);

    }






     $(".search").on("click", function()
     {

       getValue();


     });




       });
