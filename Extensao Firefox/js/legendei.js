var menu = document.querySelector("div.legendeitm-primary-menu-container-inside.clearfix");
menu.style.backgroundColor = "#000";

var ate = document.createElement("label");
ate.textContent = "Até";
ate.style.fontSize = "15px";
ate.style.color = "#FFF";

var epX_Elem = document.createElement("input");
epX_Elem.placeholder = "/Serie-S01e01/";
epX_Elem.className = "subdownlinput";


var epZ_Elem = document.createElement("input");
epZ_Elem.placeholder = "/Serie-S01e12/";
epZ_Elem.className = "subdownlinput";


var b_btn = document.createElement("span");
b_btn.textContent = "Baixar Legendas";
b_btn.className = "subdownl_span_btn";



epx = menu.appendChild(epX_Elem);
menu.appendChild(ate);
epz = menu.appendChild(epZ_Elem);

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

b_btn.addEventListener("click",function(e){
  if(epx.value.length <= 0 || epz.value.length <= 0)return;
  var EpxStr = epx.value;
  var EpzStr = epz.value;






  var x = EpxStr.match(/([^-]+)$/g)[0];
  var z = EpzStr.match(/([^-]+)$/g)[0];


  x = x.substring(1, x.length);
  z = z.substring(1, z.length);

  x = x.split("e");
  z = z.split("e");

  var serieNomeX = EpxStr;
  var serieNomeZ = EpzStr;


  if(serieNomeX[serieNomeX.length -1] == "/")serieNomeX = serieNomeX.substring(0,serieNomeX.length-1);


  if(serieNomeZ[serieNomeZ.length -1] == "/")serieNomeZ = serieNomeZ.substring(0,serieNomeZ.length-1);





  serieNomeX = serieNomeX.match(/([^\/]+)$/)[0];
  serieNomeX = serieNomeX.substring(0,serieNomeX.length-6);

  serieNomeZ = serieNomeZ.match(/([^\/]+)$/)[0];
  serieNomeZ = serieNomeZ.substring(0,serieNomeZ.length-6);

  if (serieNomeX != serieNomeZ){alert("Erro: Serie ou temporada é diferente da primeira especificada.");return;}

  var season = x[0];



  x = parseInt(x[1]);
  z = parseInt(z[1]);


  if(!(x && z))return;

  var epLista = [];

  var urlLista = [ //1 User-Agent; 2 Cookies
      btoa(navigator.userAgent).concat(";",btoa(document.cookie),"\n")
  ];

  //saida pra lista
  if(x < z){

    for (var i = x;i <= z;i++) {
      if(i < 10) {ep = "0".concat(i);}else{ep = i;}
      epLista.push(serieNomeX.concat("s",season,"e",ep));

    }

  }else{

    for (var i = x;i >= z;i--) {
      if(i < 10) {ep = "0".concat(i);}else{ep = i;}
      epLista.push(serieNomeX.concat("s",season,"e",ep));
    }

  }

  //requisita url da legenda de cada ep
for(var n = 0; n < epLista.length;n++){
      var req = new XMLHttpRequest();
      var reqUrl = "https://legendei.com".concat("/",epLista[n],"/");
      req.open( "GET", reqUrl, false );
      req.send();


      if(req.status == 200){
          parser = new DOMParser();
          var pagina = parser.parseFromString(req.response,"text/html");


          var btn_content = document.querySelector(".entry-content.clearfix");

          var btn_down = pagina.querySelector(".rcw-button-0");
          if(!btn_down)btn_down = pagina.querySelector(".buttondown");

          urlLista.push("0;".concat(
            epLista[n],
            ";",
            btn_down.href,
            ";",
            reqUrl,
            "\n"
          ));



      }
    }
  SalvarListaUrls(urlLista,serieNomeX.concat("S",season,"-legendei",".subdl"));
});

btn = menu.appendChild(b_btn);
