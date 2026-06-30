document.addEventListener("DOMContentLoaded", function () {

    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {

        locale: "pt-br",

        initialView: "dayGridMonth",

        height: "auto",

        headerToolbar: {

            left: "prev,next today",

            center: "title",

            right: "dayGridMonth,timeGridWeek,timeGridDay"

        },

        events: "/calendario/eventos",

        eventClick: function(info) {

            const evento = info.event;

            document.getElementById("modalVeiculo").innerText =
                evento.extendedProps.veiculo;

            document.getElementById("modalPlaca").innerText =
                evento.extendedProps.placa;

            document.getElementById("modalMotorista").innerText =
                evento.extendedProps.motorista;

            document.getElementById("modalDestino").innerText =
                evento.extendedProps.destino;

            document.getElementById("modalStatus").innerText =
                evento.extendedProps.status;

            document.getElementById("modalObservacoes").innerText =
                evento.extendedProps.observacoes || "-";

            document.getElementById("modalInicio").innerText =
                evento.start.toLocaleString("pt-BR");

            document.getElementById("modalFim").innerText =
                evento.end.toLocaleString("pt-BR");

            document.getElementById("btnEditar").href =
                "/agendamentos/editar/" + evento.id;

            const modal = new bootstrap.Modal(
                document.getElementById("eventoModal")
            );

            modal.show();

        }

    });

    calendar.render();

});