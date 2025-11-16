import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';

puppeteer.use(StealthPlugin());

export interface SmsMessage {
  from: string;
  message: string;
  time: string;
  verificationCode?: string;
}

export async function fetchSmsWithStealth(url: string): Promise<SmsMessage[]> {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu',
      '--window-size=1920x1080',
      '--disable-blink-features=AutomationControlled'
    ]
  });
  try {
    const page = await browser.newPage();
    await page.setExtraHTTPHeaders({
      'Accept-Language': 'en-US,en;q=0.9',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    });
    await page.setViewport({ width: 1920, height: 1080 });
    console.log(`Navigating to: ${url}`);
    await page.goto(url, {
      waitUntil: 'networkidle2',
      timeout: 60000
    });
    await new Promise(resolve => setTimeout(resolve, 5000));
    const bodyText = await page.evaluate(() => document.body.innerText);
    if (bodyText.includes('Just a moment') || bodyText.includes('Verify you are human')) {
      console.log('⚠️ Cloudflare challenge detected, waiting longer...');
      await new Promise(resolve => setTimeout(resolve, 10000));
    }
    const messages = await page.evaluate(() => {
      const results: SmsMessage[] = [];
      const selectors = [
        '.message',
        '.sms',
        '.sms-message',
        '[class*="message"]',
        'table tr',
        '.list-group-item'
      ];
      for (const selector of selectors) {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
          elements.forEach((el) => {
            const text = el.textContent || '';
            const codeMatch = text.match(/\b\d{6}\b/);
            results.push({
              from: 'unknown',
              message: text.trim(),
              time: new Date().toISOString(),
              verificationCode: codeMatch ? codeMatch[0] : undefined
            });
          });
          break;
        }
      }
      return results;
    });
    console.log(`Found ${messages.length} messages`);
    return messages;
  } catch (error) {
    console.error('Error fetching SMS:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

export async function getLatestVerificationCode(url: string): Promise<string | null> {
  const messages = await fetchSmsWithStealth(url);
  for (const msg of messages) {
    if (msg.verificationCode) {
      return msg.verificationCode;
    }
  }
  return null;
}
