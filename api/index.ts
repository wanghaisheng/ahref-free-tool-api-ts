import { NextApiRequest, NextApiResponse } from "next"
const { chromium: playwright } = require('playwright-core')
const sparticuzChromium = require("@sparticuz/chromium-min")

// Optional: If you'd like to use the legacy headless mode. "new" is the default.
sparticuzChromium.setHeadlessMode = true
// Optional: If you'd like to disable webgl, true is the default.
// sparticuzChromium.setGraphicsMode = false

const getDomain = (url: string) => {
  return new URL(url).hostname
}

const validUrl = (url: string) => {
  try {
    new URL(url)
    return true
  } catch (error) {
    return false
  }
}

const formatKeywords = (keywords: string) => {
  return keywords.replace(/\s+/g, '%20')
}

export default async function handler(
  request: NextApiRequest,
  response: NextApiResponse
) {

  const { url, query, method } = request
  const id = parseInt(query.id as string, 10)
  const name = query.name as string

  switch (method) {
    case "GET":

      if (request.url.includes('/api/kd')) {

        let inputKeywords = request.url?.replace("/api/kd", "")

        if (!inputKeywords) {
          response.status(400).send("Missing inputKeywords parameter")
          return
        }

        // Example usage
        // const inputKeywords = "sectional sofa"
        let formattedKeywords
        if (inputKeywords.includes(" ")) {
          formattedKeywords = formatKeywords(inputKeywords)
          console.log("Formatted keywords:", formattedKeywords)
        } else {
          formattedKeywords = inputKeywords
          console.log("No spaces found in inputKeywords.")
        }
        let url = 'https://ahrefs.com/keyword-difficulty/'
        try {
          const browser = await playwright.launch({
            args: sparticuzChromium.args,

            executablePath: await sparticuzChromium.executablePath("https://github.com/Sparticuz/chromium/releases/download/v123.0.0/chromium-v123.0.0-pack.tar"),
            headless: sparticuzChromium.headless,
          })
          console.log("Chromium:", await browser.version())

          const context = await browser.newContext()
          console.log("new context")

          const page = await context.newPage()
          console.log("new page")

          try {
            console.log("go to url", url)
            await page.goto(url as string)

            // await page.goto(url as string, { timeout: 60000 }) // 60 seconds timeout

            console.log(await page.title())

            await page
              .getByPlaceholder('Enter keyword')
              .fill(inputKeywords)
            console.log("fill keyword", inputKeywords)

            // Start waiting for new page before clicking. Note no await.
            const pagePromise = context.waitForEvent('page')
            await page.getByRole('button', { name: 'Check keyword' }).click()
            console.log("click submit")

            const newPage = await pagePromise
            await newPage.waitForLoadState()
            console.log(await newPage.title())

            console.log(newPage.url())

            const pdfBytes = await newPage.content()
            await browser.close()

            let fileName = formattedKeywords + ".html"

            response.setHeader("Content-Type", "application/html")
            response.setHeader(
              "Content-Disposition",
              'inline; filename="' + fileName + '"'
            )

            response.status(200).send(pdfBytes)

          } catch (error) {
            console.error('Navigation error:', error)
            // Handle the error appropriately
          }
        } catch (error: any) {
          response.status(500).json({ error: error.message })
        }
      } else {

      }

      break
    case "PUT":
      // Update or create data in your database
      response.status(200).json({ id, name: name || `User ${id}` })
      break
    default:
      response.setHeader("Allow", ["GET", "PUT"])
      response.status(405).end(`Method ${method} Not Allowed`)
  }

}
