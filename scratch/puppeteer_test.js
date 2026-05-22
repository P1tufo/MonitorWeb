const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  
  try {
    await page.goto('http://127.0.0.1:8000/analytics', { waitUntil: 'networkidle0' });
    
    // Click MB51 tab
    await page.evaluate(() => {
      document.querySelectorAll('.tab-btn')[1].click();
    });
    
    // Wait a bit
    await new Promise(r => setTimeout(r, 500));
    
    const charts = await page.evaluate(() => {
       return Array.from(document.querySelectorAll('canvas')).map(c => ({
         id: c.id,
         width: c.width,
         height: c.height,
         tabDisplay: window.getComputedStyle(c.closest('.tab-content')).display
       }));
    });
    console.log("CHARTS AFTER CLICK:", charts);
    
  } catch (err) {
    console.error("Navigation failed", err);
  }

  await browser.close();
})();
