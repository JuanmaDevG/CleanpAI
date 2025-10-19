import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // Aquí deberías hacer la llamada a tu API real
    // Por ahora, simularemos la respuesta
    const API_URL = process.env.API_URL ?? 'http://backend:8000';

    const response = await fetch(`${API_URL}/processing/file`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data, { status: 202 })
  } catch (error) {
    console.error("Error processing file:", error)
    return NextResponse.json({ error: "Error al procesar el archivo" }, { status: 500 })
  }
}
