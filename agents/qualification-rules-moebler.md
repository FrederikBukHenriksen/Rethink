This file holds the rules for judging a listing in the category `moebler` (møbler). It is shared by the search agents and the verification agent.

# Qualification rules: møbler

**UDKAST. Skal gennemgås og godkendes, før møbler søges.** Reglerne er lavet ud fra lampereglerne, ikke ud fra erfaring med møbelmarkedet.

All of these must hold:

- It is a complete piece of furniture, not a loose cushion, cover, drawer, door, leg, or other part.
- It is not described as defective, broken, stained, torn or for repair.
- It is not reserved.
- It is the target model, or a defensible match to the target designer/manufacturer. A piece without a model in the list is matched on designer and type.
- It matches `Type` when one is given (sofa, stol, lænestol, bord, skab, hylde, kommode).
- Title and description contain none of the rejected words (ignore case and obvious inflections).
- Colour or material is among the allowed ones (or clearly equivalent). If none are given, any is fine. Rejected ones are out.
- Price is not above the maximum price. Do not convert currencies unless the listing's currency and a conversion source are clear.

Judge identity from title, description, seller details and images together. Give each candidate one status:

- **Bekræftet:** model and type are supported by the listing's own evidence.
- **Sandsynlig med forbehold:** most evidence fits, but a small discrepancy or missing detail remains. State it in `Forbehold`.
- **Uklar identitet:** you cannot tell if it is the right piece.

If it is clearly not a match (wrong model, type, colour, condition, price or rejected word), do not report it.

Do not infer authenticity from appearance (designer marks, hallmarks, labels). Do not call an item authentic unless the listing establishes it.
