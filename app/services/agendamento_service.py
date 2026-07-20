from datetime import datetime
import csv
import io

from flask import Response

from app.extensions import db
from app.models import Agendamento, Veiculo
from app.services.auth_service import AuthService


class AgendamentoService:

    @staticmethod
    def juntar_data_hora(data, hora):
        return datetime.combine(data, hora)

    @staticmethod
    def veiculo_disponivel(
        veiculo_id,
        data_saida,
        hora_saida,
        data_retorno,
        hora_retorno,
        ignorar_agendamento=None
    ):

        inicio = datetime.combine(data_saida, hora_saida)
        fim = datetime.combine(data_retorno, hora_retorno)

        agendamentos = Agendamento.query.filter_by(
            veiculo_id=veiculo_id
        ).all()

        for agendamento in agendamentos:

            if ignorar_agendamento and agendamento.id == ignorar_agendamento:
                continue

            inicio_existente = datetime.combine(
                agendamento.data_saida,
                agendamento.hora_saida
            )

            fim_existente = datetime.combine(
                agendamento.data_retorno,
                agendamento.hora_retorno
            )

            if inicio < fim_existente and fim > inicio_existente:
                return False

        return True

    @staticmethod
    def veiculo_pode_ser_agendado(veiculo_id):
        """Verifica se o veículo está em condições de ser agendado."""
        veiculo = Veiculo.query.get(veiculo_id)
        if not veiculo:
            return False, "Veículo não encontrado."

        if not veiculo.ativo:
            return False, "Veículo está inativo."

        if veiculo.status == "Manutenção":
            return False, "Veículo está em manutenção."

        if veiculo.status == "Inativo":
            return False, "Veículo está inativo."

        return True, ""

    @staticmethod
    def listar():
        """Lista agendamentos. Admin vê todos, usuário comum vê só os seus."""
        if AuthService.eh_admin():
            return (
                Agendamento.query
                .order_by(
                    Agendamento.data_saida.desc(),
                    Agendamento.hora_saida.desc()
                )
                .all()
            )
        else:
            usuario = AuthService.usuario_atual()
            if usuario:
                return (
                    Agendamento.query
                    .filter_by(usuario_id=usuario.id)
                    .order_by(
                        Agendamento.data_saida.desc(),
                        Agendamento.hora_saida.desc()
                    )
                    .all()
                )
            return []

    @staticmethod
    def pode_editar(agendamento_id):
        """Verifica se o usuário atual pode editar o agendamento."""
        if AuthService.eh_admin():
            return True

        agendamento = Agendamento.query.get(agendamento_id)
        if not agendamento:
            return False

        usuario = AuthService.usuario_atual()
        if usuario and agendamento.usuario_id == usuario.id:
            return True

        return False

    @staticmethod
    def criar(form):

        # Valida status do veículo
        pode_agendar, mensagem = AgendamentoService.veiculo_pode_ser_agendado(
            form.veiculo.data
        )
        if not pode_agendar:
            return {"erro": mensagem}

        if not AgendamentoService.veiculo_disponivel(
            form.veiculo.data,
            form.data_saida.data,
            form.hora_saida.data,
            form.data_retorno.data,
            form.hora_retorno.data
        ):
            return {"erro": "conflito"}

        agendamento = Agendamento(
            veiculo_id=form.veiculo.data,
            motorista=form.motorista.data,
            destino=form.destino.data,
            motivo=form.motivo.data,
            data_saida=form.data_saida.data,
            hora_saida=form.hora_saida.data,
            data_retorno=form.data_retorno.data,
            hora_retorno=form.hora_retorno.data,
            observacoes=form.observacoes.data
        )

        # Associa ao usuário logado
        usuario = AuthService.usuario_atual()
        if usuario:
            agendamento.usuario_id = usuario.id

        db.session.add(agendamento)
        db.session.commit()

        return agendamento

    @staticmethod
    def buscar_por_id(id):

        return Agendamento.query.get_or_404(id)  

    @staticmethod
    def atualizar(id, form):

        agendamento = Agendamento.query.get_or_404(id)

        # Valida status do veículo
        pode_agendar, mensagem = AgendamentoService.veiculo_pode_ser_agendado(
            form.veiculo.data
        )
        if not pode_agendar:
            return {"erro": mensagem}

        if not AgendamentoService.veiculo_disponivel(
            form.veiculo.data,
            form.data_saida.data,
            form.hora_saida.data,
            form.data_retorno.data,
            form.hora_retorno.data,
            ignorar_agendamento=id
        ):
            return {"erro": "conflito"}

        agendamento.veiculo_id = form.veiculo.data
        agendamento.motorista = form.motorista.data
        agendamento.destino = form.destino.data
        agendamento.motivo = form.motivo.data
        agendamento.data_saida = form.data_saida.data
        agendamento.hora_saida = form.hora_saida.data
        agendamento.data_retorno = form.data_retorno.data
        agendamento.hora_retorno = form.hora_retorno.data
        agendamento.observacoes = form.observacoes.data

        db.session.commit()

        return agendamento

    @staticmethod
    def excluir(id):

        agendamento = Agendamento.query.get_or_404(id)

        agendamento.status = "Cancelado"

        db.session.commit()

    @staticmethod
    def exportar_csv():
        """Exporta agendamentos para CSV. Admin vê todos, usuário comum vê só os seus."""
        agendamentos = AgendamentoService.listar()

        output = io.StringIO()
        writer = csv.writer(output)

        # Cabeçalho
        writer.writerow([
            "ID",
            "Veículo",
            "Placa",
            "Motorista",
            "Destino",
            "Motivo",
            "Data Saída",
            "Hora Saída",
            "Data Retorno",
            "Hora Retorno",
            "Status",
            "Observações",
            "Criado Em"
        ])

        # Dados
        for a in agendamentos:
            writer.writerow([
                a.id,
                a.veiculo.modelo if a.veiculo else "",
                a.veiculo.placa if a.veiculo else "",
                a.motorista,
                a.destino,
                a.motivo or "",
                a.data_saida.strftime("%d/%m/%Y") if a.data_saida else "",
                a.hora_saida.strftime("%H:%M") if a.hora_saida else "",
                a.data_retorno.strftime("%d/%m/%Y") if a.data_retorno else "",
                a.hora_retorno.strftime("%H:%M") if a.hora_retorno else "",
                a.status,
                a.observacoes or "",
                a.criado_em.strftime("%d/%m/%Y %H:%M") if a.criado_em else ""
            ])

        output.seek(0)

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=agendamentos.csv"
            }
        )
