import { type NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const iban = searchParams.get("iban")
    const minScore = searchParams.get("min_score")

    // Construir la URL con los parámetros de búsqueda
    const API_URL = process.env.API_URL ?? 'http://backend:8000';
    const params = new URLSearchParams()
    if (iban) params.append("iban", iban)
    if (minScore) params.append("min_score", minScore)

    const response = await fetch(`${API_URL}/alerts?${params.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error fetching alerts:", error)
    return NextResponse.json({ error: "Error al obtener las alertas" }, { status: 500 })
  }
}
