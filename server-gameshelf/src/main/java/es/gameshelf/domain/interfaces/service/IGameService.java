package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.*;

import java.util.List;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IGameService {
    Game add(String title, String releaseDate, String slug, String cover, int externalRating,
              Set<Developer> developerSet, Set<Publisher> publisherSet, Set<Format> formatSet,
              Set<Platform> platformSet, Set<Genre> genreSet);
    List<Game> findAll();
    Game findById(Integer id);
    Game findByTitle(String title);
    Game findBySlug(String slug);

    List<Game> findAllByYear(Integer year);
    List<Game> findAllByPlatform(Platform platform);
    List<Game> findAllByDeveloper(Developer developer);
    List<Game> findAllByPublisher(Publisher publisher);
    List<Game> findAllByGenre(Genre genre);
    List<Game> findAllByFormat(Format format);

    List<Game> findAllByUserAlphabeticalOrder();
    List<Game> findAllByUserOldestOrder();
    List<Game> findAllByUserLatestOrder();

    boolean delete(Integer id);
    Game update(Integer id, String title, String releaseDate, String slug, String cover, int externalRating,
                Set<Developer> developerSet, Set<Publisher> publisherSet, Set<Format> formatSet,
                Set<Platform> platformSet, Set<Genre> genreSet);
}
