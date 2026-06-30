from datetime import datetime

from app.models import Agendamento


class CalendarioService:

    @staticmethod
    def eventos():

        eventos = []

        agendamentos = (
            Agendamento.query
            .filter(Agendamento.status != "Cancelado")
            .all()
        )

        for agendamento in agendamentos:

            eventos.append({

                "id": agendamento.id,

                "title": f"{agendamento.veiculo.placa} - {agendamento.motorista}",

                "start": datetime.combine(
                    agendamento.data_saida,
                    agendamento.hora_saida
                ).isoformat(),

                "end": datetime.combine(
                    agendamento.data_retorno,
                    agendamento.hora_retorno
                ).isoformat(),

                "extendedProps": {

                    "veiculo": agendamento.veiculo.modelo,

                    "placa": agendamento.veiculo.placa,

                    "motorista": agendamento.motorista,

                    "destino": agendamento.destino,

                    "status": agendamento.status,

                    "observacoes": agendamento.observacoes

                }

            })

        return eventos