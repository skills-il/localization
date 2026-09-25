# Native Mobile Apps: Regulation 35ג

## What the regulation requires

Regulation 35ג of the Equal Rights for Persons with Disabilities (Service Accessibility Accommodations) Regulations, 2013, added by the 2017 amendment:

| Sub-regulation | Rule |
|----------------|------|
| 35ג(א) | Apps for devices other than a desktop or laptop (smartphones, tablets) must meet an Israeli standard for apps, if one exists. None has been published; the IS 5568 series has only Part 1 (web content) and Part 2 (documents) |
| 35ג(ב)(1) | Until then, the IS 5568 success criteria apply as far as possible and as far as relevant to apps, and to the accessibility options the operating system makes possible |
| 35ג(ב)(2) | This applies on at least two common operating systems |
| 35ג(ב)(3) | The Commissioner may specify, by guideline, which operating systems |
| 35ג(ג) | Exemption: an app is exempt if the operator runs an identical service on a website adapted to those devices that meets the standard. The inaccessible app must then carry a link, accessible as far as possible, to that website |

Regulation 35ה also requires the accessibility statement to appear in the app itself, not only on the website.

Source: https://www.nevo.co.il/law_html/law01/500_865.htm (regulations 35ג and 35ה).

## Criterion-to-API map

Use the platform's own accessibility APIs. Wrapping a web view does not change the duty.

| WCAG / IS 5568 criterion | iOS (UIKit / SwiftUI) | Android (Views / Compose) | React Native |
|--------------------------|-----------------------|---------------------------|--------------|
| 1.1.1 Non-text content, 4.1.2 Name, role, value | `accessibilityLabel`, `accessibilityTraits`, `accessibilityValue`; SwiftUI `.accessibilityLabel(_:)`, `.accessibilityValue(_:)` | `android:contentDescription`; Compose `Modifier.semantics { contentDescription = ... }` | `accessibilityLabel`, `accessibilityRole` |
| 1.4.4 Resize text | Dynamic Type: `UIFontMetrics` and `adjustsFontForContentSizeCategory` | Size text in `sp` so it follows the system font scale | Leave system font scaling on; do not cap it for body text |
| Status announcements (dynamic content) | Post a `UIAccessibility` announcement notification | Live regions on the changing view | `accessibilityLiveRegion` (Android) |
| Hebrew RTL layout | Mirror layouts with leading/trailing constraints, not left/right | Mirror layouts with start/end, not left/right | Test with the device language set to Hebrew |

## Test tools

| Tool | Platform | Use |
|------|----------|-----|
| VoiceOver | iOS | Manual screen-reader pass in Hebrew |
| Accessibility Inspector (Xcode) | iOS | Inspect labels, traits and values; run audits |
| TalkBack | Android | Manual screen-reader pass in Hebrew |
| Accessibility Scanner | Android | On-device suggestions for labels, touch-target size and contrast |
| Espresso `AccessibilityChecks` | Android | Automated checks inside instrumented UI tests |

Run the manual passes on both operating systems you ship on, since 35ג(ב)(2) requires two.

## Documentation

| Topic | URL |
|-------|-----|
| UIKit accessibility | https://developer.apple.com/documentation/uikit/uiaccessibility |
| SwiftUI accessibility modifiers | https://developer.apple.com/documentation/swiftui/view-accessibility |
| Scaling fonts automatically (Dynamic Type) | https://developer.apple.com/documentation/uikit/scaling-fonts-automatically |
| Accessibility Inspector | https://developer.apple.com/documentation/accessibility/accessibility-inspector |
| Android: make apps more accessible | https://developer.android.com/guide/topics/ui/accessibility/apps |
| Compose semantics | https://developer.android.com/develop/ui/compose/accessibility/semantics |
| Espresso accessibility checking | https://developer.android.com/training/testing/espresso/accessibility-checking |
| Accessibility Scanner | https://support.google.com/accessibility/android/answer/6376570 |
| React Native accessibility | https://reactnative.dev/docs/accessibility |
| W3C: applying WCAG 2.2 to mobile (guidance, not Israeli law) | https://www.w3.org/TR/wcag2mobile-22/ |
