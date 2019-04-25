
var lista = document.getElementById("search_results").getElementsByTagName("tr");
const LIMITE_LEGENDA = 30 //limite maximo
// 0 == head

function SalvarListaUrls(dados,nome){


      var a = document.createElement("a");
      document.body.appendChild(a);
      a.style = "display: none";


          var blob = new Blob(dados, {type: "application/subdl"}),
          url = window.URL.createObjectURL(blob);
          a.href = url;
          a.download = nome;
          a.click();
          window.URL.revokeObjectURL(url);


}


for (var i = 0; i < lista.length; i++) {



  if(!lista[i].hasAttribute("class")){ // adiciona botao baixar legendas

    var eDownTemp = document.createElement("span");
    eDownTemp.setAttribute("iar",i);
    eDownTemp.appendChild(document.createTextNode("Baixar Legendas"));
    eDownTemp.className = "DT";
    eDownTemp.addEventListener("click",function(e){ //onclick


      //adiciona eps para baixar até perceber o separador de temporada

      var serieNome = document.title.concat(" ",e.target.parentNode.childNodes[0].textContent.trim())



      var urlLista = [ //1 User-Agent; 2 Cookies
          btoa(navigator.userAgent).concat(";",btoa(document.cookie),"\n")
      ];




      for (var x = (parseInt(e.target.attributes.iar.value)+1); x < lista.length; x++) {

        if(!lista[x].hasAttribute("class"))break;

      var ep;

      // flag tipo de arquivo a ser Baixado
      // 0 = zip
      // 1 = srt
      var tipoArquivo = "0;";


      var baixarUrl = lista[x].childNodes[2].childNodes[0].href;



      if(parseInt(lista[x].childNodes[0].children[0].textContent) < 10){
        ep = "e0".concat(lista[x].childNodes[0].children[0].textContent);

      }else{
        ep = "e".concat(lista[x].childNodes[0].children[0].textContent);
      }

      if(parseInt(lista[x].childNodes[1].textContent) >= LIMITE_LEGENDA){
        tipoArquivo = "1;"

        var req = new XMLHttpRequest();
        req.open( "GET", lista[x].childNodes[0].children[1].href, false );
        req.send();


        if(req.status == 200){

          parser = new DOMParser();
          var srtLDoc = parser.parseFromString(req.response,"text/xml");


          var srtLlista = srtLDoc.getElementById("search_results").getElementsByTagName("tr");
          var z2 = 0;
          for (var z = 1; z < srtLlista.length; z++) {
              if(srtLlista[z].style.display != "none" && srtLlista[z].hasAttribute("class")){

                urlLista.push(tipoArquivo.concat(ep,"(",z2,");",srtLlista[z].childNodes[4].childNodes[0].href,";",lista[x].childNodes[0].children[1].href,"\n"));
                //srtLista[z] = tr


                z2++;
              }
          }


        }


      }else{



          urlLista.push(tipoArquivo.concat(ep,"-",
          lista[x].childNodes[0].children[1].textContent.trim().replace(/ /g,"-"),
          ";",
          baixarUrl,
          ";",
          window.location,
          "\n"
          ));

      }









      }

      SalvarListaUrls(urlLista, (serieNome.replace(/ /g,"-")).concat(".subdl"));

    });
    lista[i].childNodes[0].appendChild(eDownTemp);
  }
}
