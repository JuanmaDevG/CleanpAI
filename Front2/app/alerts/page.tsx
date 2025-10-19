"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { ArrowLeft, Search, Loader2, AlertTriangle } from "lucide-react"
import Link from "next/link"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"

interface Alert {
  IBAN: string
  codigo_transaccion: string
  importe: number
  umbral_probabilistico: number
  IBAN_empresa_cobradora: string
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(false)
  const [ibanFilter, setIbanFilter] = useState("")
  const [minScoreFilter, setMinScoreFilter] = useState("")

  const fetchAlerts = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (ibanFilter) params.append("iban", ibanFilter)
      if (minScoreFilter) params.append("min_score", minScoreFilter)

      const response = await fetch(`/api/alerts?${params.toString()}`)
      if (!response.ok) {
        throw new Error("Error al cargar alertas")
      }
      const data = await response.json()
      setAlerts(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchAlerts()
  }, [])

  const getSeverityColor = (score: number) => {
    if (score >= 0.8) return "destructive"
    if (score >= 0.6) return "default"
    return "secondary"
  }

  const getSeverityLabel = (score: number) => {
    if (score >= 0.8) return "Alta"
    if (score >= 0.6) return "Media"
    return "Baja"
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

        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2">Lectura de Alertas</h2>
          <p className="text-muted-foreground">Monitorea y filtra alertas de transacciones sospechosas</p>
        </div>

        {/* Filters */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Filtros</CardTitle>
            <CardDescription>Filtra las alertas por IBAN o umbral de probabilidad</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="iban">IBAN</Label>
                <Input
                  id="iban"
                  placeholder="ES1234567890..."
                  value={ibanFilter}
                  onChange={(e) => setIbanFilter(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="minScore">Umbral Mínimo</Label>
                <Input
                  id="minScore"
                  type="number"
                  step="0.1"
                  min="0"
                  max="1"
                  placeholder="0.7"
                  value={minScoreFilter}
                  onChange={(e) => setMinScoreFilter(e.target.value)}
                />
              </div>
              <div className="flex items-end">
                <Button onClick={fetchAlerts} className="w-full" disabled={loading}>
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Cargando...
                    </>
                  ) : (
                    <>
                      <Search className="w-4 h-4 mr-2" />
                      Buscar
                    </>
                  )}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Alerts Table */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-primary" />
              Alertas Detectadas ({alerts.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex justify-center py-8">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
              </div>
            ) : alerts.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                No se encontraron alertas con los filtros aplicados
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>IBAN</TableHead>
                      <TableHead>Código Transacción</TableHead>
                      <TableHead className="text-right">Importe</TableHead>
                      <TableHead>Probabilidad</TableHead>
                      <TableHead>Severidad</TableHead>
                      <TableHead>Empresa Cobradora</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {alerts.map((alert, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-mono text-xs">{alert.IBAN}</TableCell>
                        <TableCell className="font-mono text-xs">{alert.codigo_transaccion}</TableCell>
                        <TableCell className="text-right font-semibold">{alert.importe.toFixed(2)} €</TableCell>
                        <TableCell>
                          <div className="flex items-center gap-2">
                            <div className="w-full bg-muted rounded-full h-2 max-w-[100px]">
                              <div
                                className="bg-primary h-2 rounded-full"
                                style={{ width: `${alert.umbral_probabilistico * 100}%` }}
                              />
                            </div>
                            <span className="text-sm font-medium">
                              {(alert.umbral_probabilistico * 100).toFixed(0)}%
                            </span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant={getSeverityColor(alert.umbral_probabilistico)}>
                            {getSeverityLabel(alert.umbral_probabilistico)}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-mono text-xs">{alert.IBAN_empresa_cobradora || "N/A"}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
