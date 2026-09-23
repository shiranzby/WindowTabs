namespace Bemo

open System
open System.Globalization
open System.Reflection
open System.Resources
open System.Threading

/// Central access point for localized UI text.
///
/// All strings live in Properties\Resources.resx (neutral / English).
/// Culture specific satellites such as Resources.zh-CN.resx or
/// Resources.ja-JP.resx are picked up automatically, based on the current
/// UI culture of the process.
///
/// Setting the environment variable WINDOWTABS_LANG to a culture name
/// (for example "zh-CN") forces that UI language regardless of the OS.
module Res =

    let private overrideCulture =
        let lang = Environment.GetEnvironmentVariable("WINDOWTABS_LANG")
        if String.IsNullOrEmpty(lang) then None
        else
            try Some(CultureInfo(lang))
            with _ -> None

    let private manager =
        ResourceManager("Properties.Resources", Assembly.GetExecutingAssembly())

    /// Returns the localized text for key.
    /// Falls back to the key itself when no entry exists, so a missing
    /// translation never results in an empty caption.
    let get (key:string) : string =
        if String.IsNullOrEmpty(key) then
            String.Empty
        else
            let value =
                match overrideCulture with
                | Some culture -> manager.GetString(key, culture)
                | None -> manager.GetString(key)
            if String.IsNullOrEmpty(value) then key else value

    /// Applies the optional WINDOWTABS_LANG override to the current thread so
    /// that ResourceManager instances created elsewhere behave consistently.
    /// Call once during startup, before any form is created.
    let applyLanguageOverride() =
        match overrideCulture with
        | Some culture -> Thread.CurrentThread.CurrentUICulture <- culture
        | None -> ()
