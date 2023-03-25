<ul class="pagination">
<li 
  class="pagination-item"
>
  <button 
    type="button" 
    class="px-3 py-2 ml-0 leading-tight text-gray-500 bg-white border border-gray-300 rounded-l-lg hover:bg-gray-100 hover:text-gray-700"
    @click="onClickFirstPage"
    :disabled="isInFirstPage"
    aria-label="Go to first page"
  >
    First
  </button>
</li>

<li
  class="pagination-item"
>
  <button 
    type="button" 
    @click="onClickPreviousPage"
    :disabled="isInFirstPage"
    aria-label="Go to previous page"
    class="px-3 py-2 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700"
  >
    Previous
  </button>
</li>

<li v-for="page in pages" class="pagination-item">
  <button 
    type="button" 
    @click="onClickPage(page.name)"
    :disabled="page.isDisabled"
    :class="{ active: isPageActive(page.name) }"
    :aria-label="`Go to page number ${page.name}`"
    class="px-3 py-2 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700"
    
  >
    {{ page.name }}
  </button>
</li>

<li class="pagination-item">
  <button 
    type="button" 
    @click="onClickNextPage"
    :disabled="isInLastPage"
    aria-label="Go to next page"
    class="px-3 py-2 leading-tight text-gray-500 bg-white border border-gray-300 hover:bg-gray-100 hover:text-gray-700"
  >
    Next
  </button>
</li>

<li class="pagination-item">
  <button 
    type="button" 
    @click="onClickLastPage"
    :disabled="isInLastPage"
    class="px-3 py-2 leading-tight text-gray-500 bg-white border border-gray-300 rounded-r-lg hover:bg-gray-100 hover:text-gray-700"
    aria-label="Go to last page"
  >
    Last
  </button>
</li>
</ul>