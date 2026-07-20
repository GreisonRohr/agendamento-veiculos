from datetime import date

from app.extensions import db
from app.models import Agendamento, Veiculo
from app.services.auth_service import AuthService


class HistoricoService:

    @staticmethod
    def buscar(data_inicio=None, data_fim=None, veiculo_id=None, motorista=None, status=None):
        """Busca agendamentos com filtros."""

        query = Agendamento.query

        # Filtro por usuário (se não for admin)
        if not AuthService.eh_admin():
            usuario = AuthService.usuario_atual()
            if usuario:
                query = query.filter_by(usuario_id=usuario.id)

        if data_inicio:
            query = query.filter(Agendamento.data_saida >= data_inicio)

        if data_fim:
            query = query.filter(Agendamento.data_saida <= data_fim)

        if veiculo_id:
            query = query.filter_by(veiculo_id=veiculo_id)

        if motorista:
            query = query.filter(Agendamento.motorista.ilike(f"%{motorista}%"))

        if status:
            query = query.filter_by(status=status)

        return query.order_by(Agendamento.data_saida.desc(), Agendamento.hora_saida.desc()).all()

    @staticmethod
    def exportar_csv(agendamentos):
        """Exporta lista de agendamentos para CSV."""
        import csv
        import io
        from flask import Response

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "ID", "Veículo", "Placa", "Motorista", "Destino",
            "Data Saída", "Hora Saída", "Data Retorno", "Hora Retorno",
            "Status", "Observações"
        ])

        for a in agendamentos:
            writer.writerow([
                a.id,
                a.veiculo.modelo if a.veiculo else "",
                a.veiculo.placa if a.veiculo else "",
                a.motorista,
                a.destino,
                a.data_saida.strftime("%d/%m/%Y") if a.data_saida else "",
                a.hora_saida.strftime("%H:%M") if a.hora_saida else "",
                a.data_retorno.strftime("%d/%m/%Y") if a.data_retorno else "",
                a.hora_retorno.strftime("%H:%M") if a.hora_retorno else "",
                a.status,
                a.observacoes or ""
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=historico.csv"}
        )
