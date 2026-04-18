from app.view.frontend.screens.relatorios.cards.card_base import CardBase

class CardProcede(CardBase):
    def __init__(self, parent, row, col, callback=None):
        super().__init__(
            parent=parent,
            row=row,
            col=col,
            texto="PROCEDE",
            icone="✅",
            cor="#00cc66",
            callback=callback
        )