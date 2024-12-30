$(document).ready(function () {
  $.getJSON("/movie/watchlist", function (data, status) {
    $(".add-to-watchlist>i").css("color", "black").removeClass("fa-solid");
    if (data?.message?.length > 0) {
      for (let id of data.message) {
        if (id) {
          $(".add-to-watchlist." + id + ">i")
            .css("color", "white")
            .addClass("fa-solid");
        }
      }
    }
  });
  $(".add-to-watchlist").click(function () {
    $.getJSON(
      "/movie/toggle_movie?movie_id=" + this.dataset.movieid,
      function (data, status) {
        $(".add-to-watchlist>i").css("color", "black").removeClass("fa-solid");
        if (data?.message?.length > 0) {
          for (let id of data.message) {
            $(".add-to-watchlist." + id + ">i")
              .css("color", "white")
              .addClass("fa-solid");
          }
        }
      }
    );
  });
  initImg = $(".watchlist-movie").first()[0].dataset.image;
  $(".watchlist-poster-preview>img").attr("src", initImg);
  $(".watchlist-movie").mouseenter(function () {
    img = this.dataset.image;
    $(".watchlist-poster-preview>img").attr("src", img);
  });
});
