"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Upload, ArrowLeft, CheckCircle2, AlertCircle, Loader2 } from "lucide-react"
import Link from "next/link"
import { Alert, AlertDescription } from "@/components/ui/alert"

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{ procesadas: number; alertas_creadas: number } | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setResult(null)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const fileContent = await file.text()
      const jsonData = JSON.parse(fileContent)

      const response = await fetch("/api/processing/file", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al procesar el archivo")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-primary">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-foreground rounded flex items-center justify-center">
              <span className="text-primary font-bold text-xl">BS</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-primary-foreground">Banco Sabadell</h1>
              <p className="text-xs text-primary-foreground/80">Portal de Gestión Interna</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-medium text-primary-foreground">Usuario Interno</p>
              <p className="text-xs text-primary-foreground/80">Departamento de Fraude</p>
            </div>
            <div className="w-10 h-10 bg-primary-foreground/20 rounded-full flex items-center justify-center">
              <span className="text-primary-foreground font-semibold">UI</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link href="/">
            <Button variant="ghost" className="gap-2">
              <ArrowLeft className="w-4 h-4" />
              Volver al inicio
            </Button>
          </Link>
        </div>

        <div className="max-w-2xl">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-foreground mb-2">Subida de Información</h2>
            <p className="text-muted-foreground">Carga archivos JSON con transacciones para análisis</p>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Cargar Archivo de Movimientos</CardTitle>
              <CardDescription>Selecciona un archivo JSON con el formato de transacciones requerido</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="file">Archivo JSON</Label>
                <Input id="file" type="file" accept=".json" onChange={handleFileChange} disabled={loading} />
                {file && <p className="text-sm text-muted-foreground">Archivo seleccionado: {file.name}</p>}
              </div>

              <Button onClick={handleUpload} disabled={!file || loading} className="w-full" size="lg">
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Procesando...
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4 mr-2" />
                    Subir y Procesar
                  </>
                )}
              </Button>

              {result && (
                <Alert className="bg-primary/10 border-primary">
                  <CheckCircle2 className="h-4 w-4 text-primary" />
                  <AlertDescription className="text-foreground">
                    <strong>Procesamiento completado:</strong>
                    <ul className="mt-2 space-y-1">
                      <li>• Transacciones procesadas: {result.procesadas}</li>
                      <li>• Alertas creadas: {result.alertas_creadas}</li>
                    </ul>
                  </AlertDescription>
                </Alert>
              )}

              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="bg-muted p-4 rounded-lg">
                <h4 className="font-semibold text-sm mb-2">Formato esperado:</h4>
                <pre className="text-xs overflow-x-auto">
                  {`{
  "transacciones": [
    {
      "IBAN": "ES1234567890...",
      "producto_map": "string",
      "empresa_cobradora_norm": "string",
      "valor": 100.50,
      "fecha": "2025-01-15",
      "recurrente": false,
      "primer_gasto_con_empresa": true,
      "codigo_transaccion": "TX-123"
    }
  ]
}`}
                </pre>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
