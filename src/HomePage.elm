module HomePage exposing (main)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Encode
import Json.Decode exposing (Decoder, map2, field, list, string)

type alias Book =
    { title : String
    , author : String}

-- VIEW
view : Model -> Html Msg
view model =
    div [ class "jumbotron" ]
        [ h1 [] [ text "Welcome to Gutenberg Project Book Recommender" ]
        , h2 [] [text "Find books similar to: "]
        , viewInput "text" "Keyword" model.keyword Keyword
        , button [ onClick SubmitForm ] [ text "Go!" ]
        , viewSearch model]

viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput t p v toMsg =
  input [ type_ t, placeholder p, value v, onInput toMsg ] []

viewSearch: Model -> Html Msg
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
        [ text "Are you looking for..." ]

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
    map2 Book
        (field "title" string)
        (field "author" string)

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
