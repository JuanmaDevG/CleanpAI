"use client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, AlertTriangle, FileText, Bell } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
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
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-2">Bienvenido al Sistema de Detección</h2>
          <p className="text-muted-foreground">Gestiona transacciones y monitorea alertas de seguridad</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 max-w-5xl">
          {/* Upload Card */}
          <Link href="/upload">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-primary">
              <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <Upload className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Subida de Información</CardTitle>
                <CardDescription>Carga archivos de movimientos bancarios para análisis de fraude</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    <span>Formato JSON de transacciones</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Detección automática de anomalías</span>
                  </div>
                </div>
                <Button className="w-full mt-6">Ir a Subida de Archivos</Button>
              </CardContent>
            </Card>
          </Link>

          {/* Alerts Card */}
          <Link href="/alerts">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-primary">
              <CardHeader>
                <div className="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4">
                  <Bell className="w-6 h-6 text-primary" />
                </div>
                <CardTitle className="text-xl">Lectura de Alertas</CardTitle>
                <CardDescription>Visualiza y filtra alertas de transacciones sospechosas</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div className="flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" />
                    <span>Filtrado por IBAN</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    <span>Tabla detallada de alertas</span>
                  </div>
                </div>
                <Button className="w-full mt-6">Ver Alertas</Button>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8 max-w-5xl">
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Alertas Activas</CardDescription>
              <CardTitle className="text-3xl text-primary">24</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Archivos Procesados Hoy</CardDescription>
              <CardTitle className="text-3xl text-primary">12</CardTitle>
            </CardHeader>
          </Card>
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>Tasa de Detección</CardDescription>
              <CardTitle className="text-3xl text-primary">94%</CardTitle>
            </CardHeader>
          </Card>
        </div>
      </main>
    </div>
  )
}
