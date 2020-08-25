module HomePage exposing (main)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode exposing (Decoder, map3, field, list, string)
import String
import List

type alias Book =
    { title : String
    , author : String
    , bookid : String}

-- VIEW
view : Model -> Html Msg
view model =
    div [ class "jumbotron" ]
        [ h1 [] [ text "Welcome to Gutenberg Project Book Recommender" ]
        , h2 [] [ text "Find books similar to: " ]
        , viewInput "text" "Keyword" model.keyword Keyword
        , button [ onClick SubmitForm ] [ text "Go!" ]
        , viewSearch model]

viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput t p v toMsg =
    input [ type_ t, placeholder p, value v, onInput toMsg ] []

viewSearch : Model -> Html Msg
viewSearch model = 
    case model.searchResponse of 
        SearchLoading ->
            div []
                [ text "Waiting..." ]
        SearchFailure ->
            div []
                [ text "Search failed, please try again." ]
        SearchSuccess list ->
            div []
                [ h3 [] [ text "Are you looking for this book?" ]
                , (case List.head list of
                    Nothing -> text "List of search results is empty!"
                    Just book -> (viewBook book))
                , h3 [] [ text "You might be interested in..."]
                --, viewResults (List.tail list)]
                , (case list of
                    [] -> text "List of search results is empty!"
                    head :: tail -> viewResults tail )
                , h5 [] [ text "Click the link to read the e-book at www.gutenber.org!" ]]

viewResults : List Book -> Html Msg
viewResults list =
    case List.head list of
        Nothing -> 
            div []
                [ text "List of search results is empty!" ]
        Just book ->
            div []
                (List.map viewBook list)

viewBook : Book -> Html Msg
viewBook book = 
    h4 [] [ a [ href (String.concat["https://www.gutenberg.org/ebooks/", book.bookid]) ] [ text (bookToString book) ] ]

-- MODEL
type alias Model =
    { keyword : String
    , searchResponse : SearchStatus}

type SearchStatus
    = SearchLoading
    | SearchFailure
    | SearchSuccess (List Book)

initialModel : Model
initialModel =
    { keyword = ""
    , searchResponse = SearchLoading
    }

init : () -> ( Model, Cmd Msg)
init _ =
    (initialModel, Cmd.none)

-- UPDATE
type Msg
    = Keyword String
    | NoOp
    | SubmitForm
    | GotSearch (Result Http.Error (List Book))

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Keyword keyword ->
            ( { model | keyword = keyword }, Cmd.none )
        NoOp ->
            ( model, Cmd.none )
        SubmitForm ->
            ( { model | searchResponse = SearchLoading }, search model)
        GotSearch result ->
            case result of
                Ok list ->
                    ({ model | searchResponse = SearchSuccess list }, Cmd.none)
                Err error ->
                    let
                        _ = Debug.log "Error is " error
                    in
                        ({ model | searchResponse = SearchFailure }, Cmd.none)

-- HTTP
search : Model -> Cmd Msg
search model =   
    Http.post
        { url = "http://0.0.0.0:5000"
        , body = Http.multipartBody [Http.stringPart "keyword" model.keyword]
        , expect = Http.expectJson GotSearch searchDecoder
        }

searchDecoder : Decoder (List Book)
searchDecoder =
    Json.Decode.list bookDecoder

bookDecoder : Decoder Book
bookDecoder = 
    map3 Book
        (field "title" string)
        (field "author" string)
        (field "bookid" string)

bookToString : Book -> String
bookToString book =
    String.concat[book.title, " by ", book.author]

-- SUBSCRIPTIONS
subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none

main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view}
