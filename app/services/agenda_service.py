from datetime import datetime, date

from app.models import Veiculo, Agendamento


class AgendaService:

    @staticmethod
    def proximas_saidas():

        return (
            Agendamento.query
            .filter(
                Agendamento.data_saida >= date.today(),
                Agendamento.status != "Cancelado"
            )
            .order_by(
                Agendamento.data_saida,
                Agendamento.hora_saida
            )
            .limit(15)
            .all()
        )

    @staticmethod
    def retornos_hoje():

        return (
            Agendamento.query
            .filter(
                Agendamento.data_retorno == date.today(),
                Agendamento.status != "Cancelado"
            )
            .order_by(
                Agendamento.hora_retorno
            )
            .all()
        )

    @staticmethod
    def manutencoes():

        return (
            Veiculo.query
            .filter_by(
                ativo=True,
                status="Manutenção"
            )
            .order_by(
                Veiculo.modelo
            )
            .all()
        )

    @staticmethod
    def veiculos_livres():

        agora = datetime.now()

        livres = []

        veiculos = Veiculo.query.filter_by(
            ativo=True,
            status="Disponível"
        ).all()

        for veiculo in veiculos:

            ocupado = False

            for agendamento in veiculo.agendamentos:

                if agendamento.status == "Cancelado":
                    continue

                inicio = datetime.combine(
                    agendamento.data_saida,
                    agendamento.hora_saida
                )

                fim = datetime.combine(
                    agendamento.data_retorno,
                    agendamento.hora_retorno
                )

                if inicio <= agora <= fim:
                    ocupado = True
                    break

            if not ocupado:
                livres.append(veiculo)

        return livres