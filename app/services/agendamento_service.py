from datetime import datetime

from app.extensions import db
from app.models import Agendamento


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
    def listar():

        return (
            Agendamento.query
            .order_by(
                Agendamento.data_saida.desc(),
                Agendamento.hora_saida.desc()
            )
            .all()
        )

    @staticmethod
    def criar(form):

        if not AgendamentoService.veiculo_disponivel(
            form.veiculo.data,
            form.data_saida.data,
            form.hora_saida.data,
            form.data_retorno.data,
            form.hora_retorno.data
        ):
            return None

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

        db.session.add(agendamento)
        db.session.commit()

        return agendamento

    @staticmethod
    def buscar_por_id(id):

        return Agendamento.query.get_or_404(id)  

    @staticmethod
    def atualizar(id, form):

        agendamento = Agendamento.query.get_or_404(id)

        if not AgendamentoService.veiculo_disponivel(
            form.veiculo.data,
            form.data_saida.data,
            form.hora_saida.data,
            form.data_retorno.data,
            form.hora_retorno.data,
            ignorar_agendamento=id
        ):
            return None

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