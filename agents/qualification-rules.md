This file holds the rules for judging a listing. They are shared by the search agents and the verification agent, so they exist in one place only.

# Qualification rules

All of these must hold:

- It is a complete lamp, not a loose shade, spare part or component.
- It is not described as defective, broken or for repair.
- It is not reserved.
- It is the target model, or a defensible match to the target designer/manufacturer.
- It matches `Type` when one is given.
- Title and description contain none of the rejected words (ignore case and obvious inflections).
- Colour is among the allowed colours (or clearly equivalent). If none are given, any colour is fine. Rejected colours are out.
- Price is not above the maximum price. Do not convert currencies unless the listing's currency and a conversion source are clear.

Judge identity from title, description, seller details and images together. Give each candidate one status:

- **Bekræftet:** model and type are supported by the listing's own evidence.
- **Sandsynlig med forbehold:** most evidence fits, but a small discrepancy or missing detail remains. State it in `Forbehold`.
- **Uklar identitet:** you cannot tell if it is the right lamp.

If it is clearly not a match (wrong model, type, colour, condition, price or rejected word), do not report it.

Do not infer authenticity from appearance. Do not call an item authentic unless the listing establishes it.
