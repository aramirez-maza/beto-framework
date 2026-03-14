# BETO-TRACE: GASTOS_PERSONALES.SEC1.INTENT.CLI_ENTRY
# CLI Entry Point — Sistema de Gastos Personales
# BETO v4.2 — TRACE_VERIFIED

import argparse
import sys
from registro import registrar_gasto
from consulta import consultar_gastos, formatear_resultado


def cmd_registrar(args):
    resultado = registrar_gasto(
        monto=args.monto,
        categoria=args.categoria,
        fecha=args.fecha,
        descripcion=args.descripcion or ""
    )
    print(resultado)


def cmd_consultar(args):
    resultado = consultar_gastos(
        categoria=args.categoria,
        fecha_inicio=args.desde,
        fecha_fin=args.hasta
    )
    print(formatear_resultado(resultado))


def main():
    parser = argparse.ArgumentParser(
        prog="gastos",
        description="Sistema de Gastos Personales — BETO v4.2"
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    # Subcomando: registrar
    reg = subparsers.add_parser("registrar", help="Registrar un nuevo gasto")
    reg.add_argument("monto", type=float, help="Monto del gasto (ej: 25.50)")
    reg.add_argument("categoria", type=str, help="Categoría (ej: Comida)")
    reg.add_argument("fecha", type=str, help="Fecha en formato YYYY-MM-DD")
    reg.add_argument("--descripcion", type=str, help="Descripción opcional")
    reg.set_defaults(func=cmd_registrar)

    # Subcomando: consultar
    con = subparsers.add_parser("consultar", help="Consultar gastos")
    con.add_argument("--categoria", type=str, help="Filtrar por categoría")
    con.add_argument("--desde", type=str, help="Fecha inicio YYYY-MM-DD")
    con.add_argument("--hasta", type=str, help="Fecha fin YYYY-MM-DD")
    con.set_defaults(func=cmd_consultar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
