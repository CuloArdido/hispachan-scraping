#!/usr/bin/env node

const request = require("request");
const cheerio = require("cheerio");
const fs = require("fs");
const argv = require("yargs").argv;

function setCharAt (str,index,chr) {
  if(index > str.length-1) return str;
  return str.substr(0,index) + chr + str.substr(index+1);
}

const pagina = new Promise((resolve, reject) => {
  let imagenes = [];
  //I'd move the tablon and hilo variables up to the top and have them be module level variables instead of only local to this function.
  //that way you can more easily have access to them in your other functions. Normally doing variables like that isn't
  //really great (having a bunch of "global" variables) but since this is a one off script and those 2 variables are never
  //overwritten anywhere, it is safe and convenient in this use case
  const tablon = argv.tablon;
  const hilo = argv.hilo;
  const url = `https://www.hispachan.org/${tablon}/res/${hilo}.html`;

  request(url, (error, resp, body) => {
    if (!error && resp.statusCode === 200) {
      let $ = cheerio.load(body);

      $("img.thumb").each((i, el) => {
        let src = el.attribs.src;
        src = src.replace("thumb", "src");
        src = setCharAt(src, src.lastIndexOf("s"), "");
        imagenes.push(src);
      });
    }
    //I would call resolve({imagenes, tablon, hilo }) here
    if (error) reject(error);
  });

  //setting a timeout here for 5 seconds and "hoping" everything is done is an anti-pattern.
  //A better way would be to call the resolve function up inside the request method right after getting all the
  //imagenes strings.
  setTimeout(() => {
    resolve({
      imagenes,
      tablon,
      hilo
    });
  }, 5000);
});

//for your use case here, making your own Promise pagina and calling .then() on it probably wasn't necessary.
//you could have put your mkdirSync and for-loop with request inside of the callback of the original request (after you load cheerio and get the 
//src urls)
pagina
  .then(respuesta => {
    console.log(respuesta);

    //This isn't too bad since this is a 1-off script. But just remember that if this was code that was being run on a 
    //server, you NEVER want to use the Sync methods. 
    //Maybe 1 way to clean it up a tiny bit would be to put all 3 of these if and mkdirSync statements into their own function
    //called ensureDirectories() or something
    if(!fs.existsSync("img/")){
      fs.mkdirSync("img/");
    }

    if (!fs.existsSync(`img/${respuesta.tablon}`)){
      fs.mkdirSync(`img/${respuesta.tablon}/`);
    }

    if (!fs.existsSync(`img/${respuesta.tablon}/${respuesta.hilo}`)){
      fs.mkdirSync(`img/${respuesta.tablon}//${respuesta.hilo}`);
    }

    for(let i = 0; i < respuesta.imagenes.length; i++) {
      request(respuesta.imagenes[i]).pipe(fs.createWriteStream(`img/${respuesta.tablon}/${respuesta.hilo}/${i}.jpg`));
    }
  })
  .catch(respuesta => {
    console.error("Hubo un error al traer la pagina\n", respuesta);
  });
