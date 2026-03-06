/* globals HTMLElement */
import apiConstructor from '../api.js'

const api = apiConstructor()

export class ApiBaseElement extends HTMLElement {
  constructor() {
    super()
    this.api = api
    this.SANITY_FUNCTION_DOCUMENT = 'sanity.function.document'
    this.SANITY_FUNCTION_MEDIA_LIBRARY_ASSET = 'sanity.function.media-library.asset'
    this.SANITY_FUNCTION_SCHEDULE = 'sanity.function.cron'
  }
}
