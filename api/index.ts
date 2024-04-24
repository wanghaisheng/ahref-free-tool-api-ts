import { NextApiRequest, NextApiResponse } from "next"
const playwright = require("playwright-aws-lambda")

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
  // replace /api/
  let inputKeywords = request.url?.replace("/kd/", "")

  if (!inputKeywords) {
    response.status(400).send("Missing inputKeywords parameter")
    return
  }

  // Example usage
  // const inputKeywords = "sectional sofa"
  const formattedKeywords = formatKeywords(inputKeywords)
  console.log(formattedKeywords) // Output: "sectional%20sofa"

  let url = 'https://ahrefs.com/keyword-difficulty/?country=us&input=' + formattedKeywords
  try {
    const browser = await playwright.launchChromium({
      headless: true,
    })
    const context = await browser.newContext()

    const page = await context.newPage()

    console.log("url", url)
    await page.goto(url as string)

    const pdfBytes = await page.content()
    await browser.close()

    let fileName = formattedKeywords + ".html"

    response.setHeader("Content-Type", "application/html")
    response.setHeader(
      "Content-Disposition",
      'inline; filename="' + fileName + '"'
    )

    response.status(200).send(pdfBytes)
  } catch (error: any) {
    response.status(500).json({ error: error.message })
  }
}
