from datetime import date

from app.models import Veiculo, Agendamento


class DashboardService:

    @staticmethod
    def indicadores():

        return {
            "total_veiculos": Veiculo.query.filter_by(
                ativo=True
            ).count(),

            "disponiveis": Veiculo.query.filter_by(
                ativo=True,
                status="Disponível"
            ).count(),

            "manutencao": Veiculo.query.filter_by(
                ativo=True,
                status="Manutenção"
            ).count(),

            "agendamentos_hoje": Agendamento.query.filter_by(
                data_saida=date.today()
            ).count(),
        }

    @staticmethod
    def proximos_agendamentos():

        return (
            Agendamento.query
            .filter(
                Agendamento.data_saida >= date.today()
            )
            .order_by(
                Agendamento.data_saida,
                Agendamento.hora_saida
            )
            .limit(10)
            .all()
        )

    @staticmethod
    def retornos_hoje():

        return (
            Agendamento.query
            .filter(
                Agendamento.data_retorno == date.today()
            )
            .order_by(
                Agendamento.hora_retorno
            )
            .all()
        )

    @staticmethod
    def proximas_revisoes():

        return (
            Veiculo.query
            .filter(
                Veiculo.proxima_revisao != None,
                Veiculo.ativo == True
            )
            .order_by(
                Veiculo.proxima_revisao
            )
            .limit(10)
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
            .all()
        )