// @ts-check

/// Imports
const puppeteer = require("puppeteer");
const axios = require("axios").default;
const fs = require("fs");
const { argv } = require("process");
const { URL } = require("url");
const winston = require("winston");

/// Constants
const NEXT_SELECTOR = ".hu5pjgll.lzf7d6o1.sp_Rvr8JgMR7Y6.sx_256f06";
const IMAGE_SELECTOR = ".gitj76qy.r9f5tntg.d2edcug0";
const SLOW_TIMEOUT = 700;
const MAX_DOWNLOADS = 5;
const PAGE_RENEW = 50;

/// Logging setup

const logger = winston.createLogger({
  level: "info",
  format: winston.format.simple(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({
      filename: "fbdownloader.log",
      options: { flags: "w" },
    }),
  ],
});

/// Util code

function filename(url) {
  const path = new URL(url).pathname;
  return path.substr(path.lastIndexOf("/") + 1);
}

/// Downloader code
async function download(url) {
  return new Promise(async (resolve, reject) => {
    let response;

    try {
      response = await axios({
        method: "get",
        url: url,
        responseType: "stream",
      });
    } catch (error) {
      reject(error);
      //return;
    }

    let ws = fs.createWriteStream("./" + filename(url));

    ws.on("finish", () => {
      resolve();
    });

    ws.on("error", (error) => {
      reject(error);
    });

    response.data.pipe(ws);
  });
}

let counter = 0;
let unlock = null;

// ALWAYS AWAIT
async function limitedDownload(url) {
  if (counter === MAX_DOWNLOADS) {
    await new Promise((resolve) => {
      unlock = resolve;
    });

    unlock = null;
    limitedDownload(url);
  } else {
    logger.info(`Downloading "${url}"`);
    counter++;

    const end = (e) => {
      if (e instanceof Error) {
        logger.error(`FAILED DOWNLOAD "${url}"`);
      } else {
        logger.info(`Finished download "${url}"`);
      }

      counter--;
      if (unlock) unlock();
    };

    download(url).then(end, end);
  }
}

/*let counter = 0;
let queued = [];

function limitedDownload(url) {
  if (counter === MAX_DOWNLOADS) {
    queued.push(url);
  } else {
    download(url)
      .then(() => {
        if (queued.length > 0) {
          limitedDownload(queued.pop());
        }
      })
      .catch(() => {});
  }
}*/

/// Main code
let untilRenew = 0;

async function main() {
  // Init
  const firstUrl = argv[2];
  const browser = await puppeteer.launch({ headless: false });
  let [page] = await browser.pages();
  //await page.setViewport({ width: 1920, height: 1080 });

  // Goto first page and wait for the image
  await page.goto(firstUrl);
  await page.waitForSelector(IMAGE_SELECTOR);

  while (true) {
    // Download source and count
    const src = await page.$eval(IMAGE_SELECTOR, (e) => e.src);
    await limitedDownload(src);
    untilRenew++;

    // Break if can not continue
    if (!(await page.$(NEXT_SELECTOR))) break;

    // Navigate to the next image
    await page.waitForTimeout(SLOW_TIMEOUT);
    await page.$eval(NEXT_SELECTOR, (e) => e.click());
    await page.waitForSelector(IMAGE_SELECTOR + `:not([src="${src}"])`);

    // Memory optimization trick (avoid fb image accumulation by closing the tab)
    if (untilRenew === PAGE_RENEW) {
      const newPage = await browser.newPage();
      await newPage.goto(page.url());
      await page.close();
      page = newPage;

      await page.waitForSelector(IMAGE_SELECTOR + `:not([src="${src}"])`);
      await page.waitForTimeout(1000);
      untilRenew = 0;
    }
  }

  await browser.close();
}

main();
